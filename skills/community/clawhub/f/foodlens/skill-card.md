## Description:

FoodLens helps an agent recognize meal photos, estimate calories and macronutrients, log meals, summarize nutrition trends, and handle user corrections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxjsxy](https://clawhub.ai/user/yxjsxy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use FoodLens to turn meal photos into nutrition estimates, daily meal logs, correction-aware totals, daily summaries, and weekly diet trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meal photos may be processed by external AI vision providers.

Mitigation: Avoid photos with sensitive background content and use the skill only where external AI processing is acceptable.

Risk: Meal history and nutrition logs may be saved under the skill workspace.

Mitigation: Periodically delete, secure, or access-control stored meal logs according to the user's privacy expectations.

Risk: Nutrition estimates from photos can be inaccurate, especially portion-size and food-identification estimates.

Mitigation: Review results, apply user corrections, and treat totals as estimates rather than medical or dietary advice.

## Reference(s):

- [FoodLens ClawHub page](https://clawhub.ai/yxjsxy/skills/foodlens)
- [Publisher profile](https://clawhub.ai/user/yxjsxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python snippets, JSON meal-log examples, and human-readable nutrition reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include estimated food items, calories, macronutrients, health scores, daily totals, summaries, and correction guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
