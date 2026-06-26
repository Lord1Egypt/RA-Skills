---
name: foodlens
description: >
  AI-powered meal photo recognition and nutrition tracking. Use when a user sends
  a food/meal photo with keywords like breakfast, lunch, dinner, snack, or
  "what did I eat". Triggers on meal photos for calorie/macro analysis, daily
  nutrition summaries, weekly diet trends, and health scoring. Supports user
  corrections, duplicate detection, and customizable nutrition goals.
---

# FoodLens — AI Meal Photo & Nutrition Tracker

## Trigger Conditions
User sends a meal/food photo with context such as:
- breakfast / lunch / dinner / snack / supper / 早饭 / 午饭 / 晚饭 / 加餐 / 零食

## Configuration
Set these paths for your deployment (defaults shown):

```
FOODLENS_DIR=~/.openclaw/workspace/skills/foodlens
FOODLENS_DATA=$FOODLENS_DIR/data          # daily JSON logs: YYYY-MM-DD.json
FOODLENS_VENV=$FOODLENS_DIR/venv
```

Nutrition goals are user-configurable. Defaults (edit `foodlens_config.json`):
- Calories: 2000 kcal/day
- Protein: 80g | Carbs: 250g | Fat: 65g

---

## Core Flow

### Step 1 — Analyze Photo (Primary)

Save the inbound photo to a temp path, then run:

```bash
cd $FOODLENS_DIR && source venv/bin/activate
python3 analyze_photo.py /path/to/photo.jpg "lunch"
```

This script:
1. Calls **GPT-4o Vision** (fallback: Gemini) to identify foods and estimate
   portion sizes using container/utensil references
2. Cross-validates against `nutrition_db` (778 foods + 197 aliases);
   if deviation > 30%, trusts the database
3. Appends the meal to `data/YYYY-MM-DD.json`
4. Outputs a formatted nutrition report

**Forward the script output directly to the user.**

---

### Step 2 — Fallback (API unavailable)

If `analyze_photo.py` fails, use the `image` tool:

```
image(
  image="/path/to/photo.jpg",
  prompt="You are a professional nutritionist. Identify all foods in this meal
  photo. Observe container size and utensils to estimate actual grams per item.
  Reference: standard takeout box 500–800 ml, bowl of rice ~150–200 g,
  stir-fried noodles ~400–500 g. List each food: name, estimated grams,
  kcal per 100 g, protein/carb/fat per 100 g."
)
```

Then write results via Python:

```bash
cd $FOODLENS_DIR && source venv/bin/activate && python3 - <<'EOF'
import json, uuid, sys
sys.path.insert(0, '.')
from foodlens import (ensure_item_nutrition, calc_total,
                      health_score_and_comment, load_day, save_day,
                      today_str, recalc_day_totals)
from datetime import datetime

date_str = today_str()
day = load_day(date_str)

# Replace with image tool results
items = [
    ensure_item_nutrition({'name': 'food name', 'grams': 300, 'source': 'image_tool'}),
]

meal_total = calc_total(items)
score, comment = health_score_and_comment(meal_total, len(items))
meal = {
    'meal_id': f'meal_{uuid.uuid4().hex[:10]}',
    'timestamp': datetime.now().isoformat(),
    'label': 'lunch',
    'items': items,
    'meal_total': meal_total,
    'health_score': score,
    'comment': comment,
}
day['meals'].append(meal)
recalc_day_totals(day)
save_day(date_str, day)
print(json.dumps({'meal': meal, 'daily_total': day['daily_total']}, ensure_ascii=False, indent=2))
EOF
```

---

### Step 3 — Format Reply

```
🍽️ [Lunch] Nutrition Analysis

🔍 Identified foods:
  • Stir-fried noodles ~400g (720 kcal)
  • Shrimp ~30g (27 kcal)
  • Chicken slices ~60g (90 kcal)

📊 Meal total:
  • Calories: 837 kcal
  • Protein: 38g | Carbs: 102g | Fat: 29g

⭐ Health score: 7/10
  Comment: ...

📈 Daily total (meal N):
  • Calories: X / [goal] kcal (X%)
  • Protein: X / [goal]g (X%)
```

---

### Step 4 — User Corrections

If user says "that's not X it's Y" or "only about Xg":
1. Re-query `nutrition_db` for the corrected food
2. Update the JSON entry
3. Reply with corrected nutrition totals

---

### Step 5 — Duplicate Detection

If the same photo is sent again, alert the user it was already logged and ask
whether to record again.

---

## Summaries

**Daily summary:**
```bash
cd $FOODLENS_DIR && source venv/bin/activate
python3 analyze_photo.py --summary today
```

**Weekly trend (last 7 days):**
```bash
cd $FOODLENS_DIR && source venv/bin/activate
python3 analyze_photo.py --weekly-summary yesterday 7
```

---

## Data Layout

| Path | Description |
|------|-------------|
| `data/YYYY-MM-DD.json` | Daily meal logs |
| `nutrition_db.py` | 778 foods + 197 aliases |
| `analyze_photo.py` | Main entry point |
| `foodlens_config.json` | User nutrition goals |
| `venv/` | Python virtual environment |
