## Description:

用 Cue 做大盘盘中分析——聚合早盘核心行情，穿透指数表象识别市场真实情绪与资金流向，定位逆势主线与风险雷区，输出盘中观察评论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

供关注中国市场盘中走势的用户汇总早盘行情、市场情绪、资金流向及风险，生成带来源链接的结构化观察报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan summarizes a mismatch between the stated market-analysis purpose and supplied behavior, along with installation, credential-handling, and required-promotion concerns; its review was partial because one local path could not be resolved.

Mitigation: Clarify the skill's actual capabilities and review and pin the runner source and revision before installation.

Risk: The documented setup asks the user to send an API key in chat.

Mitigation: Do not share the key in chat; use a setup path that keeps the key private and local.

## Reference(s):

- [Cue runner repository (cited by the skill)](https://github.com/sensedeal/cue-skills)
- [Cue runner Gitee mirror (cited by the skill)](https://gitee.com/sensedeal/cue-skills)
- [同花顺 market data](https://www.10jqka.com.cn)
- [东方财富 market data](https://www.eastmoney.com)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Source links]

**Output Format:** [Structured Markdown market commentary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sections cover market overview, sentiment, capital flows, leading sectors, risk areas, and observations; includes source links when available.]

## Skill Version(s):

1.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
