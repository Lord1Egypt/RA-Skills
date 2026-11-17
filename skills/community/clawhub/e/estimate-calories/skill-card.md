## Description:

Use this skill when estimating calories and macro-nutrients from food images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swang62](https://clawhub.ai/user/swang62)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to estimate calories, macro-nutrients, portion sizes, and meal totals from food images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food-photo calorie and macro estimates can be inaccurate because portions, ingredients, oils, sauces, and preparation methods may not be fully visible.

Mitigation: State assumptions, account for hidden calories, estimate restaurant meals conservatively, and ask the user for clarification when food items cannot be identified.

Risk: Broad food-image trigger wording may cause analysis in contexts where calorie estimation was not intended.

Mitigation: Use the skill in workflows where food-photo nutrition estimation is expected and confirm user intent when the image context is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swang62/skills/estimate-calories)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown structured meal summary with itemized nutrition estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates calories, protein, carbs, fat, fiber, visible portion sizes, assumptions, and clarification needs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
