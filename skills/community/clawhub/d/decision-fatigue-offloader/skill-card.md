## Description:

低价值日常决策卸载工具。用户说'随便''不想选''午饭吃什么''今天穿什么'时触发，读取预设规则和所在城市消费水平后直接拍板，不列利弊矩阵。最多只追问一个字段；城市未知时按默认城市或全国均值处理。触发词：不想做决定、随便、帮我选、决策疲劳、午饭吃什么、今天穿什么。

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

People who want to offload low-stakes everyday choices use this skill to get a concrete decision for meals, clothing, shopping, or leisure based on their rules and a local city cost table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save a user's city and preferences for future use without a separate consent step.

Mitigation: Require permission before saving location or preferences; review or clear references/user-rules.md after temporary travel, and keep use limited to everyday choices.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/snowhola/skills/decision-fatigue-offloader)
- [Default rules](references/default-rules.md)
- [User rules](references/user-rules.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Four-line decision card in Markdown; preference notes in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask at most one clarifying question; feedback can update user-rules.md.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
