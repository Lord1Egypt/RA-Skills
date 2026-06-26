---
name: calorie_compass
description: Estimate calorie content from food names, portion sizes, or food images.
---

Calorie Compass is a nutrition estimation skill that helps calculate the approximate calorie content of food based on different types of input.

It can work in the following ways:

1. Food name and amount  
   When the user provides the name of a food item along with its quantity, serving size, or portion description, the skill estimates the total calories.  
   Examples:
   - 2 slices of pizza
   - 1 cup of rice
   - 150 grams of grilled chicken

2. Multiple food items in one meal  
   The skill can calculate calories for a full meal by handling multiple food items together and summing the total estimated calorie intake.  
   Example:
   - 2 eggs, 2 slices of toast, and 1 banana

3. Food image-based estimation  
   If the user uploads an image of food, the skill can identify the visible food items, estimate portion sizes as closely as possible, and provide an approximate calorie count. Since image-based estimates depend on visual interpretation, the result should be presented as an estimate rather than an exact value.

4. Flexible portion understanding  
   The skill should understand common quantity formats such as:
   - grams
   - ounces
   - cups
   - pieces
   - bowls
   - slices
   - spoons
   - plates

Behavior guidelines:
- Always clarify that calorie values are estimates, especially for homemade meals, mixed dishes, and image-based inputs.
- When portion size is unclear, make a reasonable assumption and state it explicitly.
- If the food item can vary widely in calories depending on preparation method, mention the variation.
  Example: fried chicken vs grilled chicken
- When possible, provide both per-item calories and total meal calories.
- If an image contains multiple foods, identify each visible item before estimating the total.
- If confidence is low from the image, say so clearly.

Example outputs:
- “1 medium banana contains approximately 105 calories.”
- “Your meal appears to include rice, grilled chicken, and sautéed vegetables. Estimated total: 520–620 calories.”
- “Assuming this is 1 cup of cooked pasta, the calorie estimate is around 200 calories.”

Optional extension:
- The skill may also provide macronutrient estimates such as protein, carbs, and fat when enough information is available.