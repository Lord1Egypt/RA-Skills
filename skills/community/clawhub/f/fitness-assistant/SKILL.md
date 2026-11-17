---
name: fitness-assistant
description: Plan daily meals and workouts from a user's age and health profile with customizable ingredients, then schedule localized plans via OpenClaw automations.
version: 0.1.7
---

# Fitness Assistant

Builds a personalized **one-day diet plan + workout plan** from the user's age, body data, and health condition, and can deliver it every day on a schedule in the user's chosen language and timezone.

Use this skill when the user asks for:
- a daily meal/diet plan, calorie or macro targets, or a workout plan;
- recurring daily fitness messages ("send me a plan every morning", "定时发每日计划", "daily plan", etc.).

## Workflow

### 1. Opening message and profile

Send the fixed opening message for the user's language from [references/dialogues.md](references/dialogues.md) (flow and collection rules in [references/opening.md](references/opening.md)): it introduces what the skill does and which details to prepare (basics and goal, ingredient choices, training time and intensity, delivery preferences), then collect what is missing. Ask only for what is missing. Minimum required: age, sex, height, weight, activity level, goal, health conditions/limitations, dietary restrictions, ingredient choices, training experience/equipment, training time, training intensity, daily routine, timezone (IANA), language. Optional: a daily food budget with its currency. If the user says "you decide"/"随便" for an item, use the default and say so. If 3+ days have passed since the last confirmed menu/training plan, start with the three-day review dialogue in [references/dialogues.md](references/dialogues.md) instead of silently reusing saved settings.

### 2. Compute targets

Run the calculator and use its numbers:

```bash
python3 {baseDir}/scripts/plan.py --age 32 --sex male --height 178 --weight 78 --activity moderate --goal lose
```

Use `--unit imperial` for lb/in inputs and `--json` for machine-readable output. The script prints BMI, BMR, TDEE, the calorie target, and protein/fat/carbs grams. If the script cannot run, compute manually using the formulas and defaults in [references/meal-planning.md](references/meal-planning.md).

### 3. Build today's plan

- **Diet**: breakfast / lunch / dinner / optional snack split, water target, and macro-aware portions following [references/meal-planning.md](references/meal-planning.md). Offer ingredient choices per meal (protein, carbs, vegetables, fat, fruit/snack) and let the user build their own menu; use the defaults when they have no preference. When the user shares today's ingredients, recommend concrete dishes built around them. Assemble the day within ±100 kcal of the target, respect dietary restrictions and the calorie floors, and save the chosen ingredients as preferences.
- **Cost**: when the user sets a daily food budget, estimate what the items still to buy cost (ingredients already at home count as zero), show the day total against the budget with the fixed cost labels, and offer cheaper swaps when over — see [references/budget.md](references/budget.md). Never present an estimate as an exact price.
- **Workout**: one session matched to experience, equipment, preferred training time, intensity, and the most recent training log entry, following [references/training.md](references/training.md); include warm-up, main work, and cooldown.
- **Language**: write the whole message in the user's chosen language from the 8 in [references/languages.md](references/languages.md), using that file's fixed labels and the fixed dialogue scripts in [references/dialogues.md](references/dialogues.md) so every language has the same structure.
- **Safety**: this is general lifestyle guidance, not medical advice. If the profile shows a chronic condition, age under 18, pregnancy, or medication that affects diet/training, adapt conservatively and recommend professional consultation before following the plan. Never go below the calorie floors in meal-planning.md.

### 4. Schedule daily delivery (when requested)

When the user wants the plan published on a schedule:

1. Confirm the delivery time (their local clock), timezone (IANA name), language, and where to deliver (this chat or another channel).
2. Create an automation with a cron schedule plus `tz`, whose payload prompt references this skill so each run produces a fresh daily plan — see [references/scheduling.md](references/scheduling.md) for the exact tool/CLI calls and the ready-to-use prompt template.
3. Confirm the created job and tell the user the next run time; if a job already exists, update it instead of creating a duplicate.

### 5. Three-day review and training log

- Keep the date of each confirmed menu/training plan in the profile. When 3+ days have passed, the next planning request starts with the exact review dialogue from [references/dialogues.md](references/dialogues.md): keep the current plan or adjust the menu / training plan, and ask what ingredients the user has today for dish ideas.
- When the user reports a completed workout, ask for the log details with the training-log dialogue in [references/dialogues.md](references/dialogues.md), record the actual date, training time, intensity/RPE, duration, and how it felt in the training log; use the latest entry to prepare the next plan (small progression, 48 h same-muscle recovery, back off if the last session was very hard) — see [references/training.md](references/training.md).
- In a scheduled run that falls on a review day, append the review question to the delivered message instead of waiting for a separate prompt.
- Record log entries only from what the user reports; never invent sessions.

### 6. Weekly summary (Sunday 21:00)

When the user wants a weekly recap, create a recurring automation for **Sunday 21:00 in their timezone** (`0 21 * * 0` plus `tz`) with the payload in [references/scheduling.md](references/scheduling.md) and the content rules in [references/weekly-summary.md](references/weekly-summary.md). The summary covers training, nutrition, spending (only when a budget is set), and 1–3 suggestions for next week, using the fixed weekly-summary dialogue and the standard labels. Keep a single job: update the existing one instead of creating a duplicate, and tell the user the next run time.

## Boundaries

- Do not invent health data or diagnose; use only what the user reports.
- Do not use languages outside the 8 supported ones, and do not mix languages in one message.
- Do not schedule without a confirmed timezone and delivery time.
- Do not present food-cost estimates as exact prices, and never mix currencies.
- Do not add medical claims or guaranteed outcomes ("burn fat in 7 days").
