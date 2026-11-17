## Description:

Diet-log helps an agent record meals, estimate nutrients from food data, save meal history locally, and summarize intake over days, weeks, or months.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sj13818161942](https://clawhub.ai/user/sj13818161942)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to log meals, estimate calorie and nutrient intake, and generate daily, weekly, or monthly diet summaries. It is intended for general nutrition tracking and reference, not medical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meal entries can reveal health, lifestyle, and religious information and are stored persistently in plaintext.

Mitigation: Tell users where the local meal log is stored, limit collection to necessary meal details, and delete or protect references/meal_log.json when the history should not persist.

Risk: Nutrition values and food matching are estimates and may differ from actual intake or current food composition tables.

Mitigation: Present nutrition output as general reference only, ask for clarification when matching is uncertain, and avoid framing results as medical advice.

Risk: The food_data.json file is manually downloaded and could come from the wrong or modified source.

Mitigation: Have users verify the downloaded food data source before use and replace suspicious or outdated copies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sj13818161942/skills/diet-log)
- [Diet-log food data download repository](https://github.com/sj13818161942/diet-log)
- [Foodwake nutrition data source](https://github.com/LuckyHookin/foodwake)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown nutrition reports and JSON meal log/statistics data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Meal history is saved locally in references/meal_log.json, and food nutrition data must be supplied separately as references/food_data.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
