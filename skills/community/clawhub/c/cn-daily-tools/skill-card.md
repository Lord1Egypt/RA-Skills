## Description:

中文日常工具集：天气预报、汇率查询、新闻摘要、快递追踪。适合中文用户日常使用，无需API密钥，开箱即用。Use when Chinese users need weather forecasts, currency exchange rates, news summaries, or package tracking in Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[27555402-spec](https://clawhub.ai/user/27555402-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users use this skill to ask an agent for daily utility help with weather forecasts, currency exchange, Chinese news summaries, and package tracking in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather, exchange rates, news, and package tracking can be inaccurate or stale if the agent's runtime sources or tools are unavailable or outdated.

Mitigation: Use current, reputable live sources where available and present uncertainty or source links for time-sensitive answers.

Risk: The skill defaults to Chinese-language interaction, which may not fit users expecting another language.

Mitigation: Confirm the user's preferred language when the request is not clearly in Chinese.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/27555402-spec/skills/cn-daily-tools)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown-style responses with concise summaries, links when available, and direct recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live runtime sources or tools for weather, exchange rates, news, and package tracking accuracy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
