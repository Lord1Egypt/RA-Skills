---
name: fitnessrec-fitapi
description: Precise food & exercise data for AI agents — not LLM guesses. 16k foods (180 nutrients from USDA/NUTTAB/CNF2015/MEXT/FRIDA), 3M branded products with barcodes, 80k recipes in 48 languages, 5k exercises with muscle targeting. Filter/sort by any nutrient, calculate personalized daily needs. Free tier available.
triggers:
  - "search food"
  - "nutrition"
  - "calories in"
  - "protein in"
  - "exercise"
  - "barcode"
  - "foods high in"
requires:
  - apiKey
actions:
  - name: search_foods
    api: https://fitapi.fitnessrec.com/api/v1/foods/search
    method: POST
  - name: filter_foods
    api: https://fitapi.fitnessrec.com/api/v1/foods/filter
    method: POST
  - name: get_food
    api: https://fitapi.fitnessrec.com/api/v1/foods/{id}
    method: POST
  - name: search_exercises
    api: https://fitapi.fitnessrec.com/api/v1/exercises/search
    method: POST
  - name: get_exercise
    api: https://fitapi.fitnessrec.com/api/v1/exercises/{id}
    method: GET
  - name: search_dishes
    api: https://fitapi.fitnessrec.com/api/v1/dishes/search
    method: POST
  - name: search_barcode
    api: https://fitapi.fitnessrec.com/api/v1/barcode/search
    method: POST
  - name: lookup_barcode
    api: https://fitapi.fitnessrec.com/api/v1/barcode/{barcode}
    method: POST
  - name: nutrition_needs
    api: https://fitapi.fitnessrec.com/api/v1/nutrition/needs
    method: POST
---

# FitAPI — The Most Detailed Food & Exercise Database API

Ask your AI agent about any food, nutrient, exercise, or barcode — and get precise, science-grade data instead of LLM guesses.

**"How much omega-3 is in salmon?"** — FitAPI returns the exact value from curated scientific databases, not an approximation from training data.

## Setup — API key required

Before making any API calls, you need an API key. If the user hasn't configured one yet, guide them through setup:

1. **Sign up** at **https://fitapi.fitnessrec.com** — free account, no credit card needed
2. **Get the API key** from the dashboard at **https://fitapi.fitnessrec.com/dashboard**
3. **Configure this skill** with the API key

All requests are authenticated via the `Authorization: Bearer {apiKey}` header. If you get a `401` error, the key is missing or invalid — tell the user to check their key in the dashboard.

| Plan | Requests/day | Price |
|------|-------------|-------|
| Free | 10 | $0 forever |
| Paid | 500 | $9.99/year |
| Enterprise | 40,000 | $49.99/month |

All plans include every endpoint and all 47 languages.

Full interactive API docs (Swagger UI): **https://fitapi.fitnessrec.com/api/docs**

## How to use this API — pick the right tool

You have 9 tools. **Do NOT just use `search_foods` for everything.** Each tool serves a specific purpose:

| User intent | Tool to use | Why |
|---|---|---|
| "What's in chicken breast?" / "Calories in rice" | `search_foods` | Name-based lookup, returns full 180 nutrients per 100g + portions |
| "Foods highest in iron" / "High protein low carb" | `filter_foods` | Sort/rank by actual nutrient values — search can't do this |
| "Scan this barcode" / exact UPC/EAN number | `lookup_barcode` | Direct barcode → product lookup |
| "Find me a protein bar" / branded product name | `search_barcode` | Search 3M+ branded products by name |
| "How to do a deadlift?" / exercise lookup | `search_exercises` | Returns instructions, tips, muscle targeting, equipment |
| "Recipe for pad thai" / dish lookup | `search_dishes` | 80k+ recipes with ingredients matched to nutrition DB |
| "How much protein do I need?" / daily targets | `nutrition_needs` | Personalized macro/micronutrient targets from body stats |

### Recommended workflows (chain these for better answers)

**1. Meal planning — "Plan a high-protein lunch under 500 calories"**
1. `nutrition_needs` — get the user's daily targets (if body stats are known)
2. `filter_foods` — find foods matching criteria: `filter='1003 > 25 AND 1008 < 200', sort='1003:desc'`
3. Present options with portions and macros

**2. Recipe nutrition breakdown — "How many calories in caesar salad?"**
1. `search_dishes` — find the recipe, get `normalized_ingredients` with matched food IDs and gram amounts
2. Each ingredient includes `matched_id` — use `get_food` to retrieve full nutrient detail for any ingredient you need to examine
3. The dish itself already includes aggregated `nutrients` per 100g

**3. Diet comparison — "Which has more omega-3, salmon or mackerel?"**
1. `search_foods` for each food (returns full 180 nutrients including omega-3 as nutrient ID `4444`)
2. Compare the `nutrients.4444.value` fields directly

**4. Nutrient gap analysis — "Am I getting enough iron?"**
1. `nutrition_needs` — get daily iron requirement (nutrient `1089`)
2. `search_foods` for the user's logged foods — sum up iron from each
3. Compare total vs. requirement

**5. Barcode scanning — "What is this product?"**
1. `lookup_barcode` with the UPC/EAN number for direct match
2. If no match, fall back to `search_barcode` with the product name

**6. Exercise programming — "Chest exercises with dumbbells"**
1. `search_exercises` with `body_parts: ["chest"], equipments: ["Dumbbell"]`
2. Results include muscle activation percentages (`MuscleDistribution`) — use these to build balanced routines that cover all muscle groups

### Important: search_foods already returns complete data

`search_foods` returns **all 180 nutrients**, portions, and metadata per food. You do NOT need to call `get_food` after search — the data is identical. Use `get_food` only when you already have a food ID (e.g., from a recipe's `normalized_ingredients`).

### What you get

- **16,000+ foods** with 180 nutrients each — every vitamin, mineral, amino acid, fatty acid — curated from 5 international databases (USDA, NUTTAB, CNF2015, MEXT, FRIDA)
- **3 million+ branded products** — scan or search any barcode (UPC/EAN) for nutrition facts
- **80,000+ local recipes** from 48 languages — with ingredients matched to the nutrition database for accurate macros
- **5,000+ exercises** — step-by-step instructions, tips, main/granular/synergist muscles, equipment, and muscle activation percentages
- **Smart filtering** — "foods highest in iron", "high protein low fat seafood", "most omega-3" — sorted by actual nutrient values, not keyword matching
- **Personalized daily needs** — calculate exact macro/micronutrient targets based on body stats and goals
- **48 languages** — food names, exercise instructions, and recipe data translated natively

### Why not just ask the LLM?

LLMs estimate. FitAPI knows. When you ask "how much protein in chicken breast", an LLM guesses ~31g from training data. FitAPI returns 22.5g per 100g from the USDA database — the actual measured value. For serious nutrition tracking, the difference matters.

## Tools

### search_foods

Search foods by name. Returns nutrient data per 100g and portion sizes.

```
POST https://fitapi.fitnessrec.com/api/v1/foods/search
```

**Request:**
```json
{"q": "chicken breast raw", "locale": "en", "limit": 5}
```

- `q` (required): Search query in English
- `locale`: Language code for translated names (en, tr, de, fr, es, it, pt, nl, ru, ja, ko, zh, ar, hi, pl, sv, da, fi, cs, ro, hu, bg, el, hr, sr, sk, sl, bs, sq, et, lt, lv, is, nn, vi, th, id, ms, fil, uk, fa, he, bn, ka, az, mn, ur, af)
- `limit`: 1-100, default 20

**Response:** Array of foods with `id`, `desc` (name), `nutrients` map (ID -> {name, unit, value per 100g}), `portions` map.

### filter_foods

Filter and sort foods by nutrient values. Use for "which food has the most X" or "foods high in X" queries. ALWAYS include sort.

```
POST https://fitapi.fitnessrec.com/api/v1/foods/filter
```

**Request:**
```json
{"filter": "1003 > 20 AND 1004 < 5", "sort": "1003:desc", "limit": 10}
```

- `filter` (required): MeiliSearch filter expression. Operators: =, !=, >, >=, <, <=, TO, AND, OR, NOT
- `sort` (required): `nutrientId:desc` or `nutrientId:asc`
- `q`: Optional text search to narrow results
- `locale`: Language code
- `limit`: 1-100, default 20

**Example queries:**
- Highest protein: `filter='1003 > 0', sort='1003:desc'`
- Most omega-3: `filter='4444 > 0', sort='4444:desc'`
- Most omega-6: `filter='5555 > 0', sort='5555:desc'`
- Low calorie + high fiber: `filter='1008 < 100 AND 1079 > 5', sort='1079:desc'`
- High iron: `filter='1089 > 3', sort='1089:desc'`
- High protein seafood: `filter='ctg = 15 AND 1003 > 20', sort='1003:desc'`

**Nutrient IDs:**

| Category | IDs |
|----------|-----|
| Macros | 1008=calories(kcal), 1003=protein(g), 1004=fat(g), 1005=carbs(g), 1079=fiber(g), 2000=sugars(g), 1051=water(g) |
| Minerals | 1087=calcium(mg), 1089=iron(mg), 1090=magnesium(mg), 1091=phosphorus(mg), 1092=potassium(mg), 1093=sodium(mg), 1095=zinc(mg), 1098=copper(mg), 1101=manganese(mg), 1103=selenium(ug) |
| Vitamins | 1162=vitC(mg), 1165=B1(mg), 1166=B2(mg), 1167=B3(mg), 1175=B6(mg), 1177=folate(ug), 1178=B12(ug), 1106=vitA(ug), 1109=vitE(mg), 1114=vitD(ug), 1183=vitK(ug) |
| Lipids | 1253=cholesterol(mg), 1258=saturated(g), 1292=monounsat(g), 1293=polyunsat(g), 1257=trans(g), 4444=omega3(g), 5555=omega6(g) |
| Amino acids | 1210=tryptophan(g), 1212=isoleucine(g), 1213=leucine(g), 1214=lysine(g), 1219=valine(g) |

**Food categories (ctg):** 1=dairy, 2=spices, 3=baby foods, 4=fats/oils, 5=poultry, 6=soups/sauces, 7=sausages, 8=cereals, 9=fruits, 10=pork, 11=vegetables, 12=nuts/seeds, 13=beef, 14=beverages, 15=seafood, 16=legumes, 17=lamb/game, 18=baked, 19=sweets, 20=grains, 21=fast food, 22=meals, 25=snacks, 26=branded

### get_food

Get a single food by ID with full nutrient data (120+ nutrients).

```
POST https://fitapi.fitnessrec.com/api/v1/foods/{id}
```

**Request (optional body):**
```json
{"locale": "en"}
```

### search_exercises

Search 5,000+ exercises with step-by-step instructions, tips, main/granular/synergist muscle targeting, equipment, and muscle activation percentages.

```
POST https://fitapi.fitnessrec.com/api/v1/exercises/search
```

**Request:**
```json
{
  "q": "bench press",
  "locale": "en",
  "limit": 5,
  "exercise_types": ["strength_training"],
  "body_parts": ["chest"],
  "equipments": ["Barbell"]
}
```

- `q` (required): Search query
- `locale`: Language code for translated instructions/tips
- `limit`: 1-100, default 20
- `exercise_types`: strength_training, strength_training.functional, stretching
- `body_parts`: abs, arms, back, calves, cardio, chest, feet, forearms, glutes, legs, neck, plyometrics, shoulders, stretching, weightlifting, yoga
- `equipments`: Assisted, Band, Barbell, Battling Rope, Body weight, Bosu ball, Cable, Dumbbell, EZ Barbell, Hammer, Kettlebell, Leverage machine, Medicine Ball, Olympic barbell, Power Sled, Resistance Band, Roll, Rollball, Rope, Sled machine, Smith machine, Stability ball, Stick, Suspension, Trap bar, Vibrate Plate, Weighted, Wheel roller
- `targets`: Pectoralis Major Sternal Head, Deltoid Anterior, Biceps Brachii, Triceps Brachii, Latissimus Dorsi, Quadriceps, Hamstrings, Gluteus Maximus, Rectus Abdominis, Erector Spinae, etc.

**Response:** Array of exercises with `exercise` (name), `info`, `instructions[]`, `tips[]`, `Target[]`, `Synergist[]`, `Equipment[]`, `BodyPart[]`, `MuscleDistribution` (muscle -> 0.0-1.0).

### get_exercise

Get a single exercise by ID.

```
GET https://fitapi.fitnessrec.com/api/v1/exercises/{id}
```

### search_dishes

Search 80,000+ international dishes/recipes with ingredients automatically matched to the food database for accurate nutrition.

```
POST https://fitapi.fitnessrec.com/api/v1/dishes/search
```

**Request:**
```json
{"q": "caesar salad", "locale": "en", "limit": 5}
```

**Response:** Dishes with `desc`, `country`, `ingredient_count`, `normalized_ingredients[]` (matched to food DB with scores), `nutrients` per 100g, `portions`.

### search_barcode

Search branded food products by name.

```
POST https://fitapi.fitnessrec.com/api/v1/barcode/search
```

**Request:**
```json
{"q": "coca cola", "limit": 5}
```

**Response:** Branded products with `desc`, `brandOwner`, `gtinUpc`, `marketCountry`, `nutrients`, `portions`.

### lookup_barcode

Look up a specific product by barcode number.

```
POST https://fitapi.fitnessrec.com/api/v1/barcode/{barcode}
```

Example: `POST /api/v1/barcode/0041220576920`

### nutrition_needs

Calculate personalized daily macro and micronutrient needs based on body measurements.

```
POST https://fitapi.fitnessrec.com/api/v1/nutrition/needs
```

**Request:**
```json
{
  "body": {
    "weight": 80,
    "height": 180,
    "age": 30,
    "gender": "m",
    "activity_level": 3,
    "macro_target": {
      "target_type": "deficit",
      "target_amount": 300,
      "protein": 30,
      "carb": 40,
      "fat": 30
    }
  }
}
```

- `weight`: kg
- `height`: cm
- `age`: years
- `gender`: m (male), f (female), p (pregnant), l (lactating)
- `activity_level`: 1=sedentary, 2=light, 3=moderate, 4=very active, 5=extra active
- `macro_target.target_type`: maintenance, deficit, surplus
- `macro_target.target_amount`: kcal offset (for deficit/surplus)
- `macro_target.protein/carb/fat`: percentage split (sum to 100)

**Response:** Map of nutrient ID -> daily need value, plus `bmr`, `tdee`, and macro breakdown.

## Error Responses

```json
{"error": "message"}
```

| Status | Meaning |
|--------|---------|
| 401 | Invalid or missing API key |
| 429 | Rate limit exceeded |
| 502 | Search service error |

## Notes

- All nutrient values are per 100g unless portions are specified
- Portions include weight in grams and description (e.g. "1 cup", "1 breast")
- Food search queries should be in English; set `locale` to translate response names
- Food database curated from USDA, NUTTAB (Australia), CNF2015 (Canada), MEXT (Japan), FRIDA (Denmark)
- 3 million+ branded food products with barcode lookup
- 80,000+ local recipes/dishes from 48 languages with ingredient matching
- Nutrient IDs follow USDA numbering with custom extensions (4444=omega-3, 5555=omega-6)
