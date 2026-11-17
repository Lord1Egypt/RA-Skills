## Description:

用 Cue 做大盘盘中分析——聚合早盘核心行情，穿透指数表象识别市场真实情绪与资金流向，定位逆势主线与风险雷区，输出盘中观察评论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and market observers use this skill to review intraday market conditions, including broad index activity, market sentiment, fund flows, leading sectors, and potential risks. It produces a structured market commentary with source links and observational guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious, citing requests to share an API key in chat and behavior that does not match the stated market-analysis purpose; the available assessment is partial.

Mitigation: Do not paste API keys into chat. Configure credentials directly in the user's local Cue configuration or environment, and review commands before running them.

Risk: Intraday commentary and operational suggestions depend on Cue and external public data sources, whose availability, freshness, and accuracy may vary.

Mitigation: Check cited source links and current data before acting; treat the commentary as observational input and make investment decisions independently.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/panting09266-ai/skills/cue-intraday-market)
- [Cue service](https://cuecue.cn/)
- [Cue runner source (as referenced by the skill)](https://github.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Structured Markdown market commentary with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organized into market overview, sentiment, fund flows, leading sectors, risk areas, and observational guidance; includes the original report link when available.]

## Skill Version(s):

1.1.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
