---
name: body
description: >
  Physical performance — workouts, fitness tracking, nutrition, meal logging, macros, recipes.
  Use when the user mentions exercise, lifting, running, training, food, eating, macros, protein,
  meal planning, or anything related to physical health and performance.
  Routes to sub-skills: coach (movement/training) or chef (nutrition/food).
---

# Body — Physical Performance Router

This is the parent skill for Jack's Body dimension. Routes to the right sub-skill based on intent.

## Routing Logic

### → coach/
**Use for:** workouts, lifting sessions, training splits, PRs, recovery, soreness, volume, sleep,
running, mobility, Hevy data, "did I train today", "what should I train", "how am I progressing".
Triggers: /workout /pr /split /recovery /week /weight

### → chef/
**Use for:** food, eating, meals, macros, protein, calories, recipes, grocery lists, meal plans,
nutrition advice, "what should I eat", meal logging, dietary preferences.
Triggers: /meal /macros /recipe /mealplan /groceries

## Sub-skill Index

| Sub-skill | Path | Handles |
|-----------|------|---------|
| Coach | `body/coach/SKILL.md` | Training, Hevy integration, PRs, recovery, Body XP |
| Chef | `body/chef/SKILL.md` | Nutrition, meal logging, recipes, grocery lists |
| Hevy | `body/hevy/SKILL.md` | Raw Hevy API (infrastructure — used by Coach, not called directly) |

## Dimension
All XP from body sub-skills maps to the **Body 💪** dimension (STR, CON stats).
