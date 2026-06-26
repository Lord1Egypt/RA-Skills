---
name: food-balance
description: >
  Analyse a user's meal or daily food intake and give gentle, friendly suggestions on whether
  their diet is balanced and within calorie/nutrient limits. Use this skill whenever a user
  describes what they ate — a meal, a snack, a full day of eating — and wants to know if it
  is healthy, balanced, or within calorie limits. Trigger on phrases like "I ate...", "I had...
  for lunch", "is my diet balanced?", "was that too much?", "what did I eat today?", "my meal
  was...", or any description of food consumption followed by a question about health,
  calories, balance, or nutritional adequacy. Even casual descriptions like "just had pizza
  and coke" should trigger this skill if the user seems to want feedback.
---

# Food Balance Skill

Help users understand whether their meal or daily intake is nutritionally balanced and within
recommended limits. Deliver advice in a warm, encouraging, non-judgmental tone.

## Scope of application

*Asian population or people living in Asia mainly*

## Reference Files

Before analysing, load the relevant reference(s) from `references/`:

- **`nutrition_sv_guide.md`** — Japanese SV (serving) system: standard serving sizes per food
  category, calorie limits for snacks/beverages (≤200 kcal/day), and the SV counting rule.
- **`balanced_diet_hk.md`** — Hong Kong Healthy Eating Food Pyramid: recommended daily
  intakes by age group (children, teenagers, adults, elderly), food exchange list, and
  general balance principles.

Read both files. They are complementary: the SV guide gives per-meal serving benchmarks; the
HK pyramid gives daily totals by age group.

---

## Workflow

### 1. Understand the Input

Identify from the user's message:
- **What** foods were eaten (ingredients, dishes, drinks, snacks)
- **How much** (portions, bowls, glasses, pieces — estimate if vague)
- **Which meal** (breakfast / lunch / dinner / snack) or full day
- **Age group** if mentioned or inferable (default to "Adult" if unknown)

If the user's description is very vague (e.g. "I had some rice"), Politely ask **how much** like
"Could you tell me how much were eaten?".

### 2. Map to Food Categories

Using both reference guides, map each food item to one or more of these categories:

| Category | Examples |
|---|---|
| Grains | Rice, bread, noodles, pasta |
| Vegetables | Leafy greens, potatoes, mushrooms, seaweed |
| Fruits | Apples, oranges, kiwi, fruit juice (limited) |
| Fish & Meat / Protein | Meat, fish, eggs, tofu, beans |
| Milk & Dairy | Milk, yogurt, cheese |
| Fat / Oil / Sugar | Fried foods, butter, sweets, sauces |
| Snacks & Beverages | Chips, cake, alcohol, sugary drinks |

### 3. Assess Balance

Compare the user's intake against:
- **Per-meal SV targets** (from `nutrition_sv_guide.md`): grain ~40g carbs, vegetables ~70g,
  protein ~6g per SV
- **Daily totals by age group** (from `balanced_diet_hk.md`): e.g. Adults need 3–8 bowls
  grains, ≥3 servings veg, ≥2 fruit, 5–8 taels protein, 1–2 dairy, 6–8 glasses fluid
- **Snack/beverage cap**: ≤200 kcal/day for extras

Flag:
- ✅ Categories that look well covered
- ⚠️ Categories that seem low or missing
- 🔴 Anything that looks excessive (too much oil/fat, heavy snacks, alcohol)

### 4. Estimate Calories (if relevant)

If the user asks about calories or if intake looks excessive, provide a rough estimate using
common food calorie references. Keep estimates clearly approximate ("roughly X kcal").

General adult daily targets: ~1800–2200 kcal for women, ~2000–2600 kcal for men. Adjust for
age/activity if context is given.

### 5. Deliver Suggestions

Write a short, friendly response structured as:

1. **Quick summary** — one sentence on the overall picture ("Your lunch looks fairly balanced!")
2. **What's good** — briefly acknowledge what they did well (1–2 points)
3. **Gentle suggestions** — 2–3 actionable tips for what to add, reduce, or swap
4. **Calorie note** — only if relevant or asked

**Tone rules:**
- Warm and encouraging, never preachy or alarming
- Avoid absolutes ("you must", "never eat") — prefer ("you might try", "consider adding")
- Keep it concise — aim for 150–250 words unless a detailed breakdown is requested
- Use simple language, no medical jargon

---

## Example Response Shape

> **Your dinner looks pretty good overall!** 🍽️
>
> You've got a solid grain base with the rice, and the fish is a great protein source. Nice work
> including some vegetables too.
>
> A couple of gentle suggestions:
> - The portion of vegetables looks a bit light — try doubling it next time (aim for roughly
>   70g or half a bowl of cooked veg per meal).
> - The fried preparation adds quite a bit of oil. Steaming or grilling the fish occasionally
>   would keep the fat content lower.
> - A piece of fruit after the meal would round out your vitamins nicely.
>
> Calorie-wise, this meal is likely around 600–700 kcal — reasonable for dinner. 👍

---

## Edge Cases

- **Only snacks described**: Gently note the 200 kcal/day snack guideline and suggest a
  proper meal if appropriate.
- **Very restrictive eating**: Do not reinforce restriction. Acknowledge the meal and gently
  suggest adding a food group that's missing.
- **Alcohol mentioned**: Note the recommended limits from the SV guide without lecturing.
- **User mentions a health condition**: Acknowledge it briefly and recommend they consult a
  dietitian for personalised advice — don't attempt clinical dietary plans.
