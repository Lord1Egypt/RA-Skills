## Description:

AI财经日报生成助手，自动获取A股、港股、美股相关市场数据，分析大盘指数、行业板块、资金流向、外汇商品和财经要闻，并生成交互式HTML可视化日报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate daily financial market summaries and interactive HTML reports covering Chinese market indices, Hong Kong indices, sector movement, capital flow, foreign exchange, commodities, news, and upcoming financial calendar items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated financial reports may execute unsafe injected content.

Mitigation: Treat generated reports as untrusted display data, review or sanitize the HTML before sharing, and open reports only in a browser context without sensitive same-origin access.

Risk: The skill relies on mutable third-party dependencies and CDN-hosted code.

Mitigation: Run the skill in an isolated virtual environment, review and pin Python dependencies before installation, and replace CDN usage with reviewed or integrity-pinned assets where possible.

Risk: Market data and news content may be incomplete, unavailable, stale, or unsuitable for investment decisions.

Mitigation: Review generated report content against authoritative sources and keep the report's non-advisory disclaimer visible to end users.

## Reference(s):

- [AKShare API Reference for Finance Daily Report](artifact/references/akshare_apis.md)
- [财经日报 ClawHub Skill Page](https://clawhub.ai/bettermen/skills/finance-daily-report-wb)
- [bettermen ClawHub Publisher Profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, HTML file]

**Output Format:** [Markdown guidance with shell commands and a generated self-contained HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report may contain incomplete or placeholder sections when upstream market data APIs fail or return no data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
