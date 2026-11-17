# User profile

Collect only what is needed. Reuse the saved profile when one exists (agent memory / user config) and ask only for missing fields, one or two at a time. Do not hardcode private health data into this skill's files; store it in the user's profile/memory or ask each time.

## Fields

| Field | Why it is needed | Notes / defaults |
|---|---|---|
| Age | BMR equation and safety | Required. If under 18 or over 65, add extra caution and recommend professional guidance. |
| Sex | BMR equation | male / female / other |
| Height | BMI and calorie math | cm or in |
| Weight | BMI and calorie math | kg or lb |
| Activity level | TDEE multiplier | sedentary / light / moderate / active / very active |
| Goal | Calorie target | lose / maintain / gain (muscle) |
| Health conditions & limitations | Safety and plan adaptation | e.g. diabetes, hypertension, joint/knee problems, injuries, pregnancy (refer to a professional — do not plan), medication affecting diet |
| Dietary preferences / restrictions | Meal planning | vegetarian / vegan, halal, allergies, intolerances, foods they dislike |
| Ingredient preferences | Build-your-own menu | optional per-meal picks (protein / carbs / vegetables / fats / snacks) from meal-planning.md, e.g. "chicken + rice for lunch" |
| Daily food budget | Cost control | amount + currency, e.g. "¥60/day", "$15/day"; optional — see budget.md |
| Weekly summary | Reporting | default Sunday 21:00 in the user's timezone; delivery channel; see weekly-summary.md |
| Training experience & equipment | Workout plan | beginner / intermediate / advanced; gym / home / bodyweight; days available per week |
| Training time & frequency | Workout schedule | preferred days and clock, e.g. "07:00, Mon/Wed/Fri"; also determines meal timing around workouts |
| Training intensity | Workout prescription | light / moderate / high (or RPE 1-10); beginners start at light-to-moderate |
| Last plan confirmation | Three-day review cadence | date the user last confirmed a menu/training plan; review again after 3+ days |
| Today's ingredients | Dish recommendation | per-planning ask: what food is on hand today (proteins / carbs / vegetables / fats) |
| Training log | Next-plan preparation | latest sessions: date, actual training time, intensity/RPE, duration, how it felt |
| Daily routine | Schedule and meal timing | wake time, meal times, preferred workout time, bedtime |
| Timezone | Scheduling | IANA name, e.g. `Asia/Shanghai`, `America/New_York` — never abbreviations like CST/PST |
| Language | Output | one of the 8 in languages.md |

## Collection tips

- Start with the minimum set (age, sex, height, weight, activity level, goal, language, timezone), then ask about health and restrictions, framed as optional but recommended: "Any conditions or injuries I should account for? Any foods to avoid?"
- When the user picks ingredients for a menu, save those choices as preferences (e.g. "chicken + rice for lunch") so future runs reuse them; ask again only when they want to change.
- Use the opening message (references/opening.md) to tell the user what to prepare, then collect the remaining fields one or two at a time — including ingredient choices, training time, and training intensity.
- Before building a menu, ask what ingredients the user has today and recommend dishes from them (see meal-planning.md); treat it as a fresh question each day, not a saved preference.
- Ask for the daily food budget and its currency when the user wants to control cost, and store it; count only the items that still have to be bought (see budget.md).
- After a completed workout, log the actual training time, intensity, duration, and how it felt (see training.md), and use the latest entry when writing the next plan.
- If the user does not know their timezone, derive it from their device/OS, or ask for city/country and map it to an IANA name.
- If the user is a minor, has a chronic condition, is pregnant, or is on medication that affects diet/training, recommend professional medical or nutritional review before following the plan.
- Save the completed profile back to the user's profile/memory (not into the skill folder) so future runs can reuse it.
