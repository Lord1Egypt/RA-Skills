# Exercise Analysis Module

Intelligently parses user exercise information through natural language interaction, voice input, and image uploads, recognizing exercise types and estimating durations, calculating calories consumed by exercises.

## Core Capabilities

- **Semantic Analysis** - Understanding user's natural language descriptions of exercise content
- **Exercise Recognition** - Accurately recognizing exercise types in user descriptions or images
- **Entity Extraction** - Extracting key information such as exercise names, durations, and intensity levels
- **Duration Estimation** - Intelligently estimating exercise duration (minutes) based on descriptions or images
- **Calorie Expenditure Estimation** - Estimating calories consumed based on exercise type, duration, and intensity
- **Standardized Output** - Generating standardized format containing exercise information and calorie expenditure

## Exercise Estimation Principles

### Estimation Methodology

When estimating exercise calorie expenditure, intelligent evaluation should be based on the following principles:

1. **Call Exercise Search API**

Use exercise search interface to obtain accurate calorie expenditure information for exercises. This service provides detailed data for various common exercises, covering calorie expenditure information at different intensities, helping users accurately record exercise expenditure.

**API Information**
- Endpoint: /exercises/search
- Parameters:
  - query: Exercise name keyword
- Note:
  - Intelligently select search keywords based on user's current conversation language, context information, etc.

**Search Result Assessment**
- **Relevance Assessment**: After obtaining search results, must assess relevance between exercise names and query keywords, only strictly relevant results may be used as important reference
- **Adoption Assessment**:
  - Strictly relevant: Directly adopt calorie expenditure data of that result
  - Relevant but not strictly: Carefully evaluate its reference value, considering possible errors

2. **Call Exercise Analysis API**

Use exercise analysis interface, which is a more advanced integrated implementation optimized for in-depth analysis of exercise scenarios.

**API Information**
- Endpoint: /exercises/analyze
- Parameters:
  - description: Exercise content described in natural language
  - image_urls: Array of publicly accessible URLs of exercise images. When provided, the system will use image recognition to analyze the exercise.
- Note:
  - At least one of description or image_urls must be provided
  - **Original Input Pass-Through Principle (Mandatory Enforcement)**:
    - Must pass the user's original exercise description input **completely and verbatim** to the description parameter, **strictly prohibiting any form of processing**
    - Prohibited behaviors include but are not limited to:
      - Summarization (e.g., simplifying "I ran for 30 minutes, then did 20 minutes of yoga" to "running + yoga")
      - Extracting key information and rewriting (e.g., rewriting "ran about 3 kilometers or so" to "running 3km", losing uncertainty information)
      - Omitting details (e.g., simplifying "I went running, feeling a bit out of breath" to "running", losing state description)
      - Reorganizing language or adjusting expression order
      - Deleting any words, interjections, or modifiers from user input
    - Must pass the user's originally uploaded image URLs **directly** to the image_urls parameter
    - **Strictly prohibited** to perform content recognition on images and convert them to text descriptions before calling the interface, as this will result in loss of critical visual information and inaccurate analysis results
    - Judgment criteria: Any difference (regardless of size) between the description or image_urls content and the user's original input is considered a violation
  - Refer to API documentation for specific parameter formats and constraints

**Output Content**
- Exercise name, duration, calorie expenditure, intensity, and other information
- Confidence and reasoning basis, helping to decide whether to trust the result

**Multi-Exercise Processing Strategy**
- **Independent Exercise Separation**: When user description contains multiple independent exercises, should be split into multiple independent requests
  - Example: "I ran for 30 minutes, then swam for 1 hour" → Split into two independent calls
  - Judgment criteria: Exercises have clear separation, connected by parallel conjunctions such as comma or "and", and each exercise maintains independent form

**Multi-Image Processing Strategy**
- **Image Merge Upload**: When user uploads multiple images for the same exercise, all images must be merged and passed into the image parameter at once, and the exercise analysis interface will perform multimodal fusion analysis
  - Processing principles:
    - Identify whether multiple images belong to the same exercise entity
    - Integrate all related images into a single API call
    - Rely on the interface's multimodal fusion capability to comprehensively analyze complementary information in each image (duration, heart rate, distance, speed, etc.)
  - Prohibited behavior:
    - Do not split multiple images of the same exercise into multiple independent API calls, otherwise it will lead to loss of key information and inaccurate analysis results

3. **API Call Failure or No Results Handling**:
   - Roughly estimate based on public information
   - Clearly inform users of data limitations
   - When API call limit is reached, prompt users with relevant limit information and guide next steps

## Complete Processing Flow

```
User Input
    ↓
[1] Input Type Judgment
    - Text input
    - Image input
    - Text and image input
    ↓
[2] Data Acquisition
    - Call exercise analysis API:
        - Use large models for deep analysis and reasoning
        - Obtain accurate exercise type, duration, and calorie expenditure data
    - Or call exercise search API:
        - Obtain accurate calorie expenditure data through keyword search
    - When API call fails:
        - Estimate duration and calories based on common sense
        - Estimate calorie expenditure based on public information
    ↓
[3] Generate Output
    - Standardize exercise names
    - Determine final duration (minutes)
    - Output calorie expenditure estimation results
    ↓
Output Results
```

## Output Format

```json
{
  "items": [
    {
      "exercise_name": "Running",
      "duration": 30,
      "calories": 300,
      "intensity": "medium"
    }
  ]
}
```

## Tips for Improving Entry Accuracy

To help the agent more accurately recognize exercise types and assess durations, users can adopt the following methods:

### Text Input Tips
- **Detailed Description**: Provide specific exercise names, durations, and intensity levels
- **Quantitative Information**: Provide specific durations when possible, such as "30 minutes running", "1 hour swimming"
- **Avoid Ambiguous Expressions**: Use clear duration descriptions, such as "30 minutes" instead of "a while"

### Voice Input Tips
- **Clear Pronunciation**: Moderate speech rate to ensure numbers and duration units are clearly distinguishable
- **Complete Description**: Include exercise names, durations, and intensity levels
- **Quiet Environment**: Record in quiet environments to reduce background noise interference

### Image Input Tips
- **Include Exercise Equipment**: Include display information from exercise equipment (e.g., treadmills, elliptical trainers) in images
- **Photograph Exercise App Screenshots**: Photograph exercise app data interfaces, ensuring duration and calorie expenditure are clearly visible
- **Photograph Wearable Devices**: Photograph exercise data displayed on smart wristbands, watches, or other devices
- **Adequate Lighting**: Ensure images have adequate lighting and display information is clearly visible
- **Multi-angle Photography**: For complex exercise scenarios, photograph from multiple angles to provide more comprehensive information
