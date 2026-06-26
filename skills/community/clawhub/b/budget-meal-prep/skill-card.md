## Description: <br>
Weekly meal prep system for one person on a tight budget, used to eat well on $40-60/week, reduce food waste, stop relying on takeout, and batch cook for the week in 2-3 hours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtousehumans](https://clawhub.ai/user/howtousehumans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create a low-budget weekly meal-prep plan, shopping list, batch-cooking workflow, daily assembly plan, and storage guidance tailored to their budget, dietary restrictions, kitchen equipment, and food-waste concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store sensitive food budget, health, religious dietary, meal preference, pantry, weekly plan, and reminder details in agent state. <br>
Mitigation: Share only the detail needed for useful meal planning, avoid unnecessary sensitive disclosures, and review or clear stored state when it is no longer needed. <br>
Risk: Batch-cooking guidance can create food-safety risk if cooling, storage, or reheating steps are skipped or applied incorrectly. <br>
Mitigation: Keep food-safety guidance in meal-prep responses, including cooling cooked food promptly, using shallow containers, following fridge and freezer time limits, and reheating food thoroughly. <br>
Risk: Meal plans can be unsuitable if dietary restrictions, allergies, equipment limits, or very low budgets are not accounted for. <br>
Mitigation: Ask for restrictions, equipment, available storage, and budget before producing a plan; adapt substitutions and refer users to food assistance resources when budget constraints indicate food insecurity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/howtousehumans/budget-meal-prep) <br>
- [USDA SNAP-Ed Connection](https://snaped.fns.usda.gov) <br>
- [FoodSafety.gov](https://www.foodsafety.gov) <br>
- [USDA MyPlate](https://www.myplate.gov) <br>
- [NRDC food waste resources](https://www.nrdc.org) <br>
- [Feeding America food bank locator](https://findafoodbank.feedingamerica.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with checklists, meal-prep templates, shopping lists, and state fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain user budget, dietary restrictions, equipment, meal preferences, pantry status, weekly plans, reminder state, and food-insecurity flags in agent state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
