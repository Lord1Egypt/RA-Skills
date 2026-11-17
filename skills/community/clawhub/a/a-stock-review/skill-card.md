## Description:

A股股票复盘分析工具，基于AkShare库提供全面的股票复盘报告。支持行情走势、财务指标、资金流向、板块概念、技术分析等多维度分析。用于回答个股复盘、行情分析、基本面分析、技术面分析等问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianxiangbing](https://clawhub.ai/user/tianxiangbing)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to generate Chinese A-share review reports covering market price action, technical indicators, capital flow, sector context, announcements, and trading scenarios. Outputs should be treated as informational market analysis rather than personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce highly actionable trading advice, including position sizing, stop-loss, and buy/sell language.

Mitigation: Treat outputs as informational analysis only and require independent review before making investment decisions.

Risk: Market-data calls to Chinese data providers may be incomplete, stale, unavailable, or inconsistent across sources.

Mitigation: Verify ticker, company name, date, source, and key price or volume figures against trusted market-data sources before relying on the report.

Risk: The security review flags misleading or under-scoped implementation details.

Mitigation: Review the artifact behavior and dependency/data-source assumptions before deployment, especially where generated reports imply executable trading confidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianxiangbing/skills/a-stock-review)
- [Publisher profile](https://clawhub.ai/user/tianxiangbing)
- [Sina Finance quote endpoint used by artifact code](https://hq.sinajs.cn/list={self.market}{self.stock_code})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text stock analysis report with tabular market-data excerpts and trading guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current or recent market data, confidence scores, price levels, probability estimates, position sizing, stop-loss, and buy/sell language.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
