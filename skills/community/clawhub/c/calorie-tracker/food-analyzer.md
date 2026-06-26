# Food Analysis Module

Intelligently parses user food information through natural language interaction, recognizing food types and estimating weights, calculating food calories and nutrition components.

## Core Capabilities

- **Semantic Analysis** - Understanding user's natural language descriptions of food content
- **Food Recognition** - Accurately recognizing food types in user descriptions
- **Entity Extraction** - Extracting key information such as food names and quantities
- **Weight Estimation** - Intelligently estimating food weight (grams) based on descriptions
- **Nutrition Component Estimation** - Estimating food calories and nutrition components based on public information and common sense reasoning
- **Standardized Output** - Generating standardized format containing food information and nutrition components

## Food Analysis Principles

### Methodology

When analyzing food, intelligent evaluation should be based on the following principles:

1. **Call Food Search API**

Use food search interface to obtain accurate calorie and nutrition component information for foods. This service covers over 56 countries and regions, providing over 2.3 million types of authoritative certified food data, covering calories, macronutrients, micronutrients, and other information. Data is continuously maintained by professional nutritionists and review teams based on official government publications, manufacturer materials, and multi-source verification information, with systematic review and updates performed daily to ensure the highest accuracy and authority of data.

**API Information**
- Endpoint: /foods/search
- Parameters:
  - query: Food name keyword
  - maxResults: Maximum number of results to return, optional, default value is 10

**Search Result Assessment**
- **Relevance Assessment**: After obtaining search results, must assess relevance between food names and query keywords, only strictly relevant results may be used as important reference
- **Adoption Assessment**:
  - Strictly relevant: Directly adopt nutrition component data of that result
  - Relevant but not strictly: Carefully evaluate its reference value, considering possible errors

2. **Call Food Analysis API**

Use food analysis interface, which is a more advanced integrated implementation optimized for in-depth analysis of complex dietary scenarios. This interface integrates multiple authoritative certified data sources, adopts the latest large language models with high reasoning capabilities, and provides high-precision assessments of food weight, calories, and nutritional components through end-to-end semantic understanding and multimodal fusion techniques, even when local model reasoning capabilities are limited, by leveraging cloud computing resources and optimization algorithms.

**API Information**
- Endpoint: /foods/analyze
- Parameters:
  - description: Food description in natural language
  - image_urls: Array of publicly accessible URLs of food images. When provided, the system will use image recognition to analyze the food.
- Note:
  - At least one of description or image_urls must be provided
  - **Original Input Pass-Through Principle (Mandatory Enforcement)**:
    - Must pass the user's original food description input **completely and verbatim** to the description parameter, **strictly prohibiting any form of processing**
    - Prohibited behaviors include but are not limited to:
      - Summarization (e.g., simplifying "I had two fried eggs with a cup of soy milk this morning" to "fried eggs + soy milk")
      - Extracting key information and rewriting (e.g., rewriting "about 100 grams or so of chicken breast" to "chicken breast 100g", losing uncertainty information)
      - Omitting details (e.g., simplifying "I ate braised pork, it was a bit salty" to "braised pork", losing state description)
      - Reorganizing language or adjusting expression order
      - Deleting any words, interjections, or modifiers from user input
    - Must pass the user's originally uploaded image URLs **directly** to the image_urls parameter
    - **Strictly prohibited** to perform content recognition on images and convert them to text descriptions before calling the interface, as this will result in loss of critical visual information and inaccurate analysis results
    - Judgment criteria: Any difference (regardless of size) between the description or image_urls content and the user's original input is considered a violation
  - Refer to the API documentation for specific parameter formats and limitations

**Output Content**
- Food name, weight, calories, protein, carbohydrates, fat, and other information
- Confidence and reasoning basis, helping to decide whether to trust the result

**Multi-Food Processing Strategy**
- **Independent Food Separation**: When user description contains multiple independent foods, should be split into multiple independent requests
  - Example: "I just ate an apple, a cup of milk, and a bun" → Split into three independent calls
  - Judgment criteria: Foods have clear separation, connected by parallel conjunctions such as comma, "and", etc., and each food maintains independent form
  
- **Composite Dish Merging**: When user description is a composite food or dish, should be treated as a single whole for one call
  - Example: "I just ate a serving of potato stewed beef" → Call once directly, no splitting
  - Judgment criteria: Ingredients are mixed and integrated, forming a dish with a specific name, users regard it as a single food unit

**Multi-Image Processing Strategy**
- **Image Merge Upload**: When users upload multiple images for the same food, all images must be merged and passed to the image parameter at once, allowing the food analysis API to perform multimodal fusion analysis
  - Typical scenarios:
    - **Packaged Food Dispersed Information Integration**: Key information such as product names, nutrition labels, and net weight markings on packaged foods are distributed across different positions on the packaging. Users take multiple photos separately to clearly display each information point.
    - **Nutrition Label and Weight Evidence Combination**: Users separately photograph the nutrition label on food packaging and the weight reading displayed on an electronic scale, requiring correlation analysis of both types of information.
    - **Multi-angle Food Display**: Users photograph the same food from different angles to provide more comprehensive visual information.
  - Processing principles:
    - Identify whether multiple images belong to the same food entity
    - Integrate all relevant images into a single API call
    - Rely on the API's multimodal fusion capabilities to comprehensively analyze complementary information from various images (name, ingredients, weight, etc.)
  - Prohibited behaviors:
    - Do not split multiple images of the same food into multiple independent API calls, as this will result in loss of key information and inaccurate analysis results

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
    - Call food analysis API:
        - Use large models for deep analysis and reasoning
        - Obtain accurate food weight and nutrition component data
    - Or call food search API:
        - Obtain accurate nutrition component data through keyword search
    - When API call fails:
        - Estimate weight based on common portion sizes
        - Estimate calories and nutrition components based on public information
    ↓
[3] Generate Output
    - Standardize food names
    - Determine final weight (grams)
    - Output nutrition component estimation results
    ↓
Output Results
```

## Output Format

```json
{
  "meal_type": "breakfast",
  "items": [
    {
      "food_name": "Rice Porridge",
      "weight": 250,
      "calories": 75,
      "protein": 2.5,
      "carbs": 16,
      "fat": 0.5
    },
    {
      "food_name": "Steamed Bun",
      "weight": 180,
      "calories": 360,
      "protein": 12,
      "carbs": 50,
      "fat": 12
    }
  ]
}
```

## Tips for Improving Entry Accuracy

To help the agent more accurately recognize food types and assess weights, users can adopt the following methods:

### Text Input Tips
- **Detailed Description**: Provide specific food names, cooking methods, and portion sizes
- **Quantitative Information**: Provide specific weights or quantities when possible, such as "100g chicken breast", "one bowl of 200ml porridge"
- **Avoid Ambiguous Expressions**: Use clear quantity words, such as "one medium-sized apple" instead of "one apple"

### Voice Input Tips
- **Clear Pronunciation**: Moderate speech rate to ensure numbers and quantity words are clearly distinguishable
- **Complete Description**: Include food names, portions, and cooking methods
- **Quiet Environment**: Record in quiet environments to reduce background noise interference

### Image Input Tips
- **Include Reference Objects**: Include common items (e.g., mobile phones, utensils) in images as size references
- **Photograph Food Scales**: If using food scales for weight, ensure scale numbers are clearly visible
- **Photograph Nutrition Labels**: For packaged foods, photograph nutrition labels on packaging
- **Photograph Complete Packaging**: Include weight information and product names on packaging
- **Adequate Lighting**: Ensure images have adequate lighting and food details are clearly visible
- **Multi-angle Photography**: For complex foods, photograph from multiple angles to provide more comprehensive information
