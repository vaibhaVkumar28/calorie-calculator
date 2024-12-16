from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the Google Gemini Vision API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Use gemini-1.5-flash
    response = model.generate_content([input_prompt, image, prompt])
    return response.text

# Function to prepare the image for API
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_part = {
            "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
            "data": bytes_data
        }
        return image_part  # Return a single dictionary
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")

# Input fields
input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""
# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Predefined prompt
input_prompt = """
You are an expert nutritionist. Analyze the food items in the image and calculate the total calories and protein.Also provide some ideas to improve diet. 
Provide details of each item in the following format:

1. Item 1 - X calories
2. Item 2 - Y calories
----
Total Calories: Z
"""

# Submit button
submit=st.button("Tell me the total calories")

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt, image_data, input_prompt) 
    st.subheader("The Response is")
    st.write(response)