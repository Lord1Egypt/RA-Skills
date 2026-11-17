## Description:

Weekly meal prep system for one person on a tight budget. Use when someone wants to eat well on $40-60/week, reduce food waste, stop relying on takeout, or batch cook for the week in 2-3 hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to build a weekly meal-prep plan for one person on a tight food budget, including a shopping list, batch-cooking workflow, daily assembly formula, storage guidance, and substitutions for dietary restrictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses unpinned npx package resolution.

Mitigation: Review the package source and pin or otherwise control the installed release before using it in a sensitive environment.

Risk: The skill may store personal meal-planning details such as budget, dietary restrictions, pantry state, weekly history, and reminders.

Mitigation: Collect only the details needed for planning, avoid unnecessary sensitive health information, and clear stored state when it is no longer needed.

Risk: Batch-cooking advice can create food-safety risk if cooling, storage, or reheating guidance is skipped.

Mitigation: Keep food-safety guidance in batch-cooking and storage responses, especially cooling, refrigerator life, freezing, and reheating checks.

Risk: Meal plans may conflict with allergies, dietary restrictions, equipment limits, or severe food insecurity if the initial assessment is incomplete.

Mitigation: Ask about restrictions, equipment, storage space, budget, and food-assistance needs before generating a weekly plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/budget-meal-prep)
- [USDA SNAP-Ed Connection](https://snaped.fns.usda.gov)
- [FoodSafety.gov](https://www.foodsafety.gov)
- [USDA MyPlate](https://www.myplate.gov)
- [NRDC food waste resources](https://www.nrdc.org)
- [Bureau of Labor Statistics Consumer Expenditure Surveys](https://www.bls.gov/cex/)
- [Feeding America food bank locator](https://findafoodbank.feedingamerica.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown responses with questions, checklists, shopping lists, meal plans, storage guidance, and state or reminder snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist meal-prep preferences, budget, dietary restrictions, pantry status, weekly history, and reminder state when supported by the host agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
