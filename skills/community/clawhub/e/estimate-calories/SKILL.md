---
name: estimate-calories
description: Use this skill when estimating calories and macro-nutrients from food images
---

# Estimate Calories Skill

When the user sends a food image, estimate how many calories it is visually, use your best judgement and best guess based on context and your experience as an expert nutritionist.

## When the user sends a food image

1. **Analyze the image** using your built-in vision capabilities:
   - Identify every food item visible in the image, try to name it with a descriptive title
   - Estimate portion sizes (everything in grams, including volume)
   - Calculate: Calories, Protein (g), Carbs (g), Fat (g), Fiber (g)

2. **Respond with a structured summary (example):**

   ```
   🍽️ [Date/Time] | [Meal_Type] Logged!
   
   📸 Items detected:
   - [Food item name 1]: [portion size] — [calories] kcal (Protein: [x]g | Carbs: [x]g | Fat: [x]g | Fiber: [x]g)
   - [Food item name 2]: [portion size] — [calories] kcal (Protein: [x]g | Carbs: [x]g | Fat: [x]g | Fiber: [x]g)
   ...

   📊 Meal Total: [total] kcal
   Protein: [x]g | Carbs: [x]g | Fat: [x]g | Fiber: [x]g
   ```

## Vision Analysis Guidelines

- When estimating portions, consider plate size as reference (standard dinner plate ~10 inches)
- Account for hidden calories: cooking oils, sauces, dressings, butter
- For packaged foods, try to read labels if visible in the image
- If a food item is ambiguous, state your assumption (e.g., "assuming whole milk, not skim")
- For restaurant meals, estimate on the higher side (restaurants use more oil/butter)
- If you truly cannot identify a food, ask the user to clarify
