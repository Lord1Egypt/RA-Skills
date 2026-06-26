# Fridge Chef 🤖🍳

Identify food items from a photo of your fridge and get recipe suggestions.

## Usage

User sends an image of their fridge with the message: "what can I make?"

The agent will:
1. Identify all visible food items
2. Note any items that may be expiring soon
3. Suggest 3-5 recipes using the available ingredients
4. Provide a detailed recipe when the user picks one

## Response Format

### Step 1: Food Inventory
List identified items by category:
- 🥛 Dairy: item, item
- 🥬 Produce: item, item  
- 🌭 Meat: item, item
- 🫙 Pantry: item, item

### Step 2: Expiring Soon
Flag any items that typically spoil soon (fresh herbs, salad greens, yogurt, etc.)

### Step 3: Recipe Suggestions
Present 3-5 recipe options with brief descriptions, numbered.

### Step 4: Detailed Recipe
When user picks a recipe number, provide:
- Ingredients list
- Step-by-step instructions
- Cooking time
- Serving size

## Notes
- Be specific when identifying items (e.g., "sharp cheddar" not just "cheese")
- If ingredients are unclear from the image, note them as "likely X"
- Consider common substitutions when items are missing
- Keep recipes simple and practical for home cooking

## Examples

**User:** [image of fridge] "What can I make?"

**Agent:**
"I see:
- 🥛 Dairy: mozzarella, yogurt, cream
- 🥬 Produce: salad greens, tomatoes, carrots
- 🌭 Meat: chorizo
- 🫙 Pantry: canned tomatoes, olives

**Recipe ideas:**
1. Pasta al pomodoro (canned tomatoes + mozzarella + garlic)
2. Chorizo + carrot sheet pan (15 min)
3. Greek salad with whatever greens you have"

Select 1-3 for full recipe.
