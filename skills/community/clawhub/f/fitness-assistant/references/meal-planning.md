# Meal planning rules

## Safety boundaries (non-negotiable)

- This is general lifestyle guidance, not medical advice. Never diagnose or treat.
- Pregnant, nursing, under 18, chronic illness, or medication that affects diet: recommend consulting a doctor/dietitian before following the plan.
- Calorie floor: never plan below **1,200 kcal/day (female)** or **1,500 kcal/day (male)**; use **1,600+ kcal for adults 65+**. If the computed target is below the floor, use the floor and explain why.
- Healthy weight-loss pace is about **0.25–0.5 kg/week** (a deficit of ~250–500 kcal/day). Never exceed a **750 kcal/day deficit**.
- Always include hydration; never plan skipped meals.

## Numbers (script output; manual fallback below)

- BMI = weight(kg) / height(m)²
- BMR (Mifflin-St Jeor): men `10w + 6.25h − 5a + 5`; women `10w + 6.25h − 5a − 161` (w = kg, h = cm, a = years)
- TDEE = BMR × activity multiplier:

| Activity | Multiplier |
|---|---|
| Sedentary (desk, little exercise) | 1.2 |
| Light (1–3 sessions/week) | 1.375 |
| Moderate (3–5 sessions/week) | 1.55 |
| Active (6–7 sessions/week) | 1.725 |
| Very active (physical job + training) | 1.9 |

- Calorie target: lose = TDEE − 400 (deficit capped at 750, floored); maintain = TDEE; gain = TDEE + 250
- Macros: protein **1.6–2.2 g/kg** body weight (higher end when training or losing weight; 0.8–1.0 for sedentary maintenance); fat **20–35% of calories** (at least ~0.6 g/kg); carbs = remaining calories ÷ 4 g. Fiber ≥ 25–30 g. Water ≈ 30–35 ml/kg (about 2–3 L for most adults).

## Day structure

- Three main meals + 1–2 snacks, roughly: breakfast 25%, lunch 35%, dinner 30%, snacks 10%. Adjust to the user's routine — e.g. an early-morning workout moves more calories to pre/post-training.
- Every meal should contain: lean protein (about a palm), vegetables (half the plate), whole-grain/starchy carbs (about a fist, adjusted to the calorie target), healthy fat (about a thumb), plus fruit/dairy where allowed.

## Food groups and swaps

| Group | Examples | Notes |
|---|---|---|
| Protein | chicken, fish, eggs, lean beef, tofu, tempeh, lentils, chickpeas, dairy, soy milk | Vegetarian/vegan: tofu, tempeh, lentils, chickpeas, soy products, beans |
| Carbs | rice, oats, whole-wheat bread, potatoes, noodles, quinoa, fruit | Prefer whole grains; spread intake across meals |
| Vegetables | all vegetables, leafy greens | Half of each plate |
| Fats | olive oil, nuts, seeds, avocado | Small portions |

- Restrictions: halal (halal-certified meat), vegetarian/vegan (plant proteins), lactose-intolerant (dairy-free alternatives), gluten-sensitive (rice, quinoa, gluten-free oats).
- Hypertension: reduce sodium, prefer fresh over processed food. Diabetes: spread carbs evenly across meals, prefer low-GI sources, avoid sugary drinks. Keep this general and refer to a professional for medication-related advice.

## Ingredient choices (build-your-own menu)

After computing the calorie/macro targets, let the user build their own menu:

1. Show choices per meal in the user's language — one protein, one carb, vegetables, one fat, plus an optional fruit/snack — as a compact list (not the full table) using the options below.
2. Let the user pick. If they say "you choose"/"随便", pick the defaults (marked ★) and say so.
3. Assemble the day so totals land within **±100 kcal** of the calorie target with macros staying close, adjusting serving sizes rather than dropping foods. If a preferred food is calorie-dense, use a smaller portion — never skip the protein.
4. Respect restrictions and disliked foods from the profile; ask before introducing something new.
5. Save the chosen ingredients as the user's preferences so future runs reuse them; ask again only when the user wants to change.

Approximate values per serving (cooked weights unless noted); scale portions ±20–50% to fit the day's target:

| Category | Ingredient (serving) | kcal | Protein | Carbs | Fat |
|---|---|---|---|---|---|
| Protein ★ | Chicken breast, 100 g | 165 | 31 | 0 | 3.6 |
| Protein | Lean beef, 100 g | 217 | 26 | 0 | 12 |
| Protein | Salmon, 100 g | 208 | 20 | 0 | 13 |
| Protein | White fish (cod), 100 g | 82 | 18 | 0 | 0.7 |
| Protein | Eggs, 2 medium | 143 | 13 | 1 | 9.5 |
| Protein | Tofu, 100 g | 76 | 8 | 2 | 4.8 |
| Protein | Tempeh, 100 g | 193 | 19 | 9 | 11 |
| Protein | Lentils, cooked 150 g | 174 | 14 | 30 | 0.6 |
| Protein | Chickpeas, cooked 150 g | 246 | 13 | 41 | 3.6 |
| Protein | Greek yogurt, 150 g | 97 | 14 | 5 | 0.3 |
| Carbs ★ | Rice, cooked 150 g | 195 | 4 | 43 | 0.4 |
| Carbs | Oats, dry 50 g | 190 | 7 | 33 | 3 |
| Carbs | Whole-wheat bread, 2 slices | 160 | 7 | 27 | 2 |
| Carbs | Sweet potato, 150 g | 135 | 3 | 31 | 0.2 |
| Carbs | Potatoes, boiled 150 g | 130 | 3 | 30 | 0.2 |
| Carbs | Whole-wheat pasta, cooked 150 g | 210 | 8 | 40 | 1.5 |
| Carbs | Quinoa, cooked 150 g | 170 | 6 | 30 | 2.7 |
| Vegetables ★ | Broccoli, 150 g | 51 | 4 | 10 | 0.6 |
| Vegetables | Leafy greens, 100 g | 23 | 3 | 4 | 0.4 |
| Vegetables | Mixed stir-fry veg, 150 g | 45 | 2 | 8 | 0.5 |
| Fats ★ | Olive oil, 10 g | 88 | 0 | 0 | 10 |
| Fats | Almonds, 25 g | 145 | 5 | 5 | 12.5 |
| Fats | Peanut butter, 20 g | 120 | 5 | 4 | 10 |
| Fats | Avocado, 50 g | 80 | 1 | 4 | 7.5 |
| Fats | Chia/flax seeds, 15 g | 75 | 2.5 | 4 | 5.5 |
| Fruit/snack ★ | Apple, 1 medium | 95 | 0.5 | 25 | 0.3 |
| Fruit/snack | Banana, 1 medium | 105 | 1 | 27 | 0.4 |
| Fruit/snack | Berries, 100 g | 50 | 1 | 12 | 0.3 |
| Fruit/snack | Low-fat yogurt, 150 g | 100 | 10 | 12 | 0.7 |

## Today's ingredients and dish ideas

- When the user lists what they have on hand today, build each meal from those items first: pick a protein, carbs, vegetables, and a fat from the list and name a concrete dish (e.g. "chicken, broccoli, rice → chicken-broccoli rice bowl"); write dish names in the user's language.
- Estimate macros for any ingredient not in the table from common values. If an item does not fit a food group, use it only as a minor addition and keep the protein + vegetables + carbs structure.
- If a whole group is missing from the user's list (e.g. no carbs or no protein), suggest one or two simple substitutes they likely have.
- If the user gives no ingredients, fall back to their saved ingredient preferences or the defaults above.
- When a daily budget is set, favour the cheaper items above, reuse one purchased ingredient across meals, and price only what still has to be bought — see [references/budget.md](references/budget.md).

## Regional dish styles by language

When naming dishes, match the cuisine style of the user's chosen language (region is a guide, not a strict rule) and adapt it to what the user has today:

| Language | Cuisine style to draw from | Typical dish shapes |
|---|---|---|
| English (en) | International / Western | grilled or pan-fried protein + grains + salad; wrap or grain bowl; oats with fruit |
| 中文 (zh-CN) | Chinese home cooking | stir-fry + rice or noodles; rice bowl (盖浇饭-style); steamed fish + greens |
| Español (es) | Latin American / Spanish | rice + beans + grilled meat; burrito-style bowl; tortilla/quesadilla with vegetables |
| हिन्दी (hi) | Indian | dal + rice or roti; vegetable or chickpea curry; curd/raita as a side |
| Français (fr) | French / Mediterranean | fish or chicken + vegetables + whole-grain bread; vegetable soup; balanced plate |
| العربية (ar) | Middle Eastern / North African | grilled meat + rice or bulgur; hummus + salad + whole-wheat pita; lentil soup |
| Português (pt) | Brazilian / Portuguese | rice + beans + grilled protein; lighter feijoada-style stew with vegetables |
| Русский (ru) | Eastern European | buckwheat + protein; vegetable soup; kefir/cottage cheese; baked fish + potatoes |

- Use the cuisine only as a style guide: the actual protein, carbs, and vegetables still come from today's ingredients and the calorie/macro targets. Do not force exotic substitutions.
- Write dish names in the chosen language; keep well-known regional names in their original spelling where natural (e.g. "bowl", "盖浇饭", "burrito", "dal", "hummus", "гречка").

## Sample day (~2,000 kcal) — adapt portions to the computed target

- Breakfast: oats + milk/soy milk + fruit + a few nuts
- Lunch: rice + chicken/fish/tofu + vegetables + oil
- Snack: yogurt or fruit
- Dinner: whole-wheat noodles + eggs/tofu + vegetables
- Water: 2–2.5 L spread through the day
