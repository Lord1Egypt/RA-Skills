## Description:

用 Cue 帮你看清被套的股票上方还有哪几道坎——从筹码分布定位套牢盘、用均线校验阻力强度、推演反弹每一步需要的量能，产出可复核的解套压力线底稿，辅助判断反弹到哪容易卡住、哪里该减仓。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

面向希望复核个股反弹阻力的投资者，分析上方套牢筹码、均线共振位置和逐级反弹所需量能，并形成结构化报告供其参考。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports that setup asks users to share an API key in chat and that a command sends the locally stored key to a remote service; it rates the release suspicious.

Mitigation: Avoid installation until the key-handling instructions and remote request have been reviewed. Never paste a reusable API key into chat; use a revocable key and rotate it if exposed.

Risk: The security scan is partial because a referenced local path was missing, so the available evidence is incomplete.

Mitigation: Review the missing referenced file and complete a security scan before use.

Risk: Market-data freshness and external source availability can affect the analysis, and resistance estimates are not guarantees of future prices.

Mitigation: Check each report's data cutoff and source links, corroborate important figures, and treat the analysis as reference material rather than a trading instruction.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/panting09266-ai/skills/cue-unwind-pressure-line)
- [Cue platform](https://cuecue.cn)
- [Cue research runner source (listed by the skill)](https://github.com/sensedeal/cue-skills)
- [Cue research runner mirror (listed by the skill)](https://gitee.com/sensedeal/cue-skills)
- [同花顺 market data](https://www.10jqka.com.cn)
- [东方财富 market data](https://www.eastmoney.com)
- [雪球 market discussion](https://xueqiu.com)
- [TradingView charting](https://www.tradingview.com)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown report with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes resistance zones and estimated volume needs; conclusions depend on available market data and its stated cutoff date.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
