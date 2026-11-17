## Description:

BigFood helps an agent identify ingredients from user-provided food or fridge photos, recommend recipes, suggest shopping items, and provide meal-planning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn food photos or typed ingredient lists into practical recipe options, shopping suggestions, and meal-planning guidance. It is suited for recipe help and fridge inventory conversations, not precise nutrition, freshness, or food-safety decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ingredient recognition, freshness labels, and calorie estimates may be inaccurate or incomplete.

Mitigation: Use the skill for recipe ideation only; users should verify freshness, allergens, cooking safety, and nutritional needs before preparing or eating food.

Risk: Broad Chinese food and cooking triggers may activate the skill outside a narrow recipe-request context.

Mitigation: Deploy it where broad recipe assistance is acceptable and make clear that outputs are suggestions, not health or food-safety advice.

## Reference(s):

- [BigFood ClawHub skill page](https://clawhub.ai/kobenfang/skills/bigfood)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown recipe recommendations, ingredient lists, shopping suggestions, and calorie estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided photos or ingredient descriptions; no executable code, external backend, credential use, or cross-session persistence is identified in security evidence.]

## Skill Version(s):

0.1.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
