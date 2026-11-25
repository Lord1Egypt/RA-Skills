## Description:

用 Cue 分析热门赛道与 A 股 ETF，包括赛道全景、ETF 对比、持仓穿透、估值水位和风险扫描。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

A-share ETF investors, advisers, and researchers use this skill to examine sector structure, compare ETFs, review underlying holdings, and understand historical valuation levels. It provides research context rather than buy or sell timing advice.

### Deployment Geography for Use:

China (A-share listed ETFs)

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious and reports prompts to share an API key in chat.

Mitigation: Do not paste reusable API keys into chat; configure credentials through a trusted private channel and rotate them if exposed.

Risk: ClawScan reports promotional prompts and possible differences between the stated investment purpose and some demonstrated actions.

Mitigation: Review each requested action and command before running it, and confirm it fits the intended ETF research task.

Risk: The security scan was partial because a referenced local path could not be resolved, so the evidence is incomplete.

Mitigation: Review referenced files and commands and complete a full security scan before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/panting09266-ai/skills/cue-sector-etf)
- [Cue platform](https://cuecue.cn)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Structured Markdown research report with comparison tables, valuation context, risk notes, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers A-share listed ETFs; excludes buy/sell timing advice and real-time intraday NAV or arbitrage analysis. Data quality and timeliness depend on Cue and the availability of public ETF and index data.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
