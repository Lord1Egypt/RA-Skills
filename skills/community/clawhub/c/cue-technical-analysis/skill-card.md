## Description:

用 Cue 对个股做短线走势与技术面分析——从量价关系、资金流向、趋势结构入手，计算波动率与最大回撤，产出可复核的走势分析底稿，辅助判断短线的买卖节奏和关键价位。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

面向希望复盘个股短线走势的使用者，汇总量价关系、资金流向、趋势结构、波动率、最大回撤及支撑压力位，形成可复核的分析报告以辅助判断。报告提供参考信息，不代替用户作出交易决策。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security assessment says the skill asks users to share an API key in chat.

Mitigation: Avoid sending secrets in chat; use a protected local configuration if available, and review how the service handles the key before use.

Risk: The supplied security assessment says the workflow includes referral and purchase prompts beyond technical analysis.

Mitigation: Review scheduled-task and commercial prompts before acting on them; do not enable a scheduled task without choosing its settings.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/panting09266-ai/skills/cue-technical-analysis)
- [Cue platform](https://cuecue.cn)
- [Cue runner repository](https://github.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Structured Markdown report with analysis sections and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the Cue report link when the service returns one; decision support rather than a buy or sell instruction.]

## Skill Version(s):

1.1.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
