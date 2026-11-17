## Description:

北京天气早安助手：获取今日北京天气并给出穿衣和饮食建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tieemo](https://clawhub.ai/user/tieemo)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this Chinese-language assistant to get a concise Beijing morning briefing with current weather, clothing suggestions, and food or drink advice for commuting, school, exercise, or daily planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate from generic morning greetings even when the user did not intend to request a Beijing weather briefing.

Mitigation: Installers should narrow the trigger or require an explicit Beijing weather, clothing, or diet intent if generic greetings should not launch weather lookups.

Risk: Weather and air quality data can be unavailable, delayed, or inconsistent across public sources.

Mitigation: The response should state uncertainty, avoid claiming sensor-grade real-time data, and provide only general seasonal guidance when current data cannot be fetched.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tieemo/skills/beijing-morning-weather)
- [Artifact examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Chinese Markdown weather briefing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes weather summary, clothing recommendations, diet suggestions, and uncertainty language when exact current weather is unavailable.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
