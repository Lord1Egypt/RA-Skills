## Description:

Query real-time A-share stock prices, major indices, and sector data across Shanghai, Shenzhen, and Beijing exchanges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts use this skill to look up China A-share stocks and indices, then format informational quote summaries for Shanghai, Shenzhen, and Beijing exchanges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to Sina Finance for requested stock or index codes.

Mitigation: Use it only where outbound market-data requests are acceptable, and avoid entering secrets or unrelated personal data into quote queries.

Risk: Returned prices may be live, delayed, or last-close market data and could be mistaken for financial advice.

Mitigation: Present quote results as informational market data and verify important trading or investment decisions with authoritative sources.

## Reference(s):

- [China Stock Quotes on ClawHub](https://clawhub.ai/zhaocaixia888/skills/china-stock-quotes)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list=sh600519,sz300750,sh600036)
- [Sina Finance real-time stock page example](https://finance.sina.com.cn/realstock/company/sh600519/nc.shtml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown quote summaries with optional curl or PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reflect live or last-close market data from Sina Finance and should be treated as informational, not financial advice.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
