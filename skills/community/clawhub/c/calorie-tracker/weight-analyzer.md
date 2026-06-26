# Weight Analysis Module

Intelligently parses user weight information through natural language interaction, recording weight data and analyzing weight change trends to provide users with weight management references.

## Core Capabilities

- **Semantic Analysis** - Understanding user's natural language descriptions of weight content
- **Weight Recording** - Accurately recording weight data from user descriptions or images
- **Entity Extraction** - Extracting key information such as weight values, measurement times, and weight scale types
- **Trend Analysis** - Analyzing user weight change trends and providing health recommendations
- **Standardized Output** - Generating standardized format containing weight information and change trends

## Weight Data Estimation Principles

### Estimation Methodology

When processing weight data, intelligent evaluation should be based on the following principles:

1. **Based on Common Sense and Public Data**: Reference healthy weight ranges, BMI calculation standards, and other authoritative data, combined with user information for analysis.

2. **Consider Weight Description Semantics**: Accurately understand weight values and units in user descriptions (e.g., "60 kg", "130 jin", "180 lbs"), and judge actual weight based on context.

3. **Comprehensive User Characteristics**: Consider factors affecting weight such as user age, gender, height, and body fat percentage. For example:
   - Healthy weight ranges differ for different age groups
   - Body fat percentage standards differ for different genders
   - Height impact on weight (through BMI calculation)

4. **Prioritize Explicit Numerical Values**: If users provide specific weight values and units, directly use those values.

5. **Estimation Uncertainty**: For ambiguous descriptions, request clarification from users when necessary to ensure result accuracy and reliability.

### Estimation Accuracy Requirements

- Prioritize authoritative data sources
- Maintain consistency and interpretability of data recording
- All weight data must be accurate and reliable
- Pay attention to accuracy of unit conversions (e.g., kg to jin, lbs)

## Complete Processing Flow

```
User Input
    ↓
[1] Input Type Judgment
    - Text input
    - Image input
    - Text and image input
    ↓
[2] Semantic Analysis
    - Recognize weight description intent
    - Extract weight-related descriptions
    ↓
[3] Entity Recognition
    - Extract weight values
    - Identify units (kg, jin, lbs, etc.)
    - Identify measurement times (today, yesterday, last week, etc.)
    ↓
[4] Weight Data Processing
    - Extract weight values and units based on descriptions
    - Unit conversion (if necessary)
    - Calculate BMI (if height information is provided)
    ↓
[5] Trend Analysis
    - Compare with historical weight data
    - Analyze weight change trends
    - Calculate change rates
    ↓
[6] Generate Output
    - Standardize weight values
    - Determine final units
    - Output weight analysis results and trends
    ↓
Output Results
```

## Output Format

```json
{
  "items": [
    {
      "weight": 60,
      "unit": "kg",
      "date": "2023-10-01",
      "bmi": 22.5,
      "status": "Normal"
    }
  ]
}
```


## Tips for Improving Entry Accuracy

To help the agent more accurately record and analyze weight data, users can adopt the following methods:

### Text Input Tips
- **Detailed Description**: Provide specific weight values and units, such as "60 kg", "130 jin"
- **Include Time**: Provide measurement times when possible, such as "weight today is 60 kg"
- **Provide Height**: If BMI calculation is needed, provide height information, such as "height 170 cm, weight 60 kg"

### Voice Input Tips
- **Clear Pronunciation**: Moderate speech rate to ensure numbers and units are clearly distinguishable
- **Complete Description**: Include weight values, units, and measurement times
- **Quiet Environment**: Record in quiet environments to reduce background noise interference

### Image Input Tips
- **Photograph Weight Scales**: Ensure weight scale numbers are clearly visible
- **Photograph Health Apps**: Photograph health app weight data interfaces, ensuring values are clearly visible
- **Photograph Wearable Devices**: Photograph weight data displayed on smart wristbands, watches, or other devices
- **Adequate Lighting**: Ensure images have adequate lighting and display information is clearly visible
- **Photograph Complete Interfaces**: Include weight values, units, and measurement times
