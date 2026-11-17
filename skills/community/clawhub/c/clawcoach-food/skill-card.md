## Description:

Food photo analysis and meal logging for ClawCoach. Send a photo of your meal and get instant macro breakdown via Claude Vision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[authoredniko](https://clawhub.ai/user/authoredniko)

### License/Terms of Use:


## Use Case:

External users use this skill to analyze meal photos or text food descriptions, estimate calories and macronutrients, confirm meal entries, and maintain a local ClawCoach food log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous photos or casual food prompts may be interpreted as meal-logging requests.

Mitigation: Review the proposed food analysis before confirming and use edit or redo when the estimate is wrong.

Risk: Confirmed meals create a local dietary history.

Mitigation: Install only if local food logging is desired, and review or remove entries in ~/.clawcoach/food-log.json when needed.

Risk: Nutrition estimates can be inaccurate when portions or foods are unclear.

Mitigation: Confirm portions and request clarification for unclear items before saving a meal.

## Reference(s):

- [ClawCoach Food on ClawHub](https://clawhub.ai/authoredniko/skills/clawcoach-food)
- [ClawCoach project homepage](https://github.com/clawcoach/clawcoach)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown-style conversational responses with meal estimates, confirmation prompts, and local log guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ANTHROPIC_API_KEY for the OpenClaw environment; confirmed meals are stored locally under ~/.clawcoach/food-log.json.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
