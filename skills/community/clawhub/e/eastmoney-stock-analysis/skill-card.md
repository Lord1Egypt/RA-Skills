## Description:

Generates structured Chinese technical analysis reports for stock requests by retrieving public Eastmoney market data and formatting the findings into a report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyuqi98](https://clawhub.ai/user/zhangyuqi98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather public Eastmoney stock quote data and produce concise technical analysis reports for A-share, Hong Kong, or U.S. stock requests. The output is informational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some Eastmoney quote API calls use unencrypted HTTP, so market data could be unavailable, inaccurate, or tampered with in transit.

Mitigation: Prefer browser page snapshots or trusted market sources when possible, clearly mark unavailable fields, and avoid relying on a single API response.

Risk: Generated stock reports may be mistaken for investment advice.

Mitigation: Keep the report informational, include the required disclaimer, and require users to verify market data and decisions independently.

Risk: Technical indicators such as MACD, KDJ, and RSI may be missing unless historical data is retrieved and calculated.

Mitigation: Label unsupported indicators as unavailable or compute them only from validated historical price data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangyuqi98/skills/eastmoney-stock-analysis)
- [Report Template](artifact/references/report-template.md)
- [Eastmoney Stock Quote Page](https://quote.eastmoney.com/sz{code}.html)
- [Eastmoney Stock Quote API](http://push2.eastmoney.com/api/qt/stock/get?secid=0.{code}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f170,f171)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown technical analysis report with data-fetching commands and Chinese prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an informational-only disclaimer; missing or unsupported market data should be labeled as unavailable rather than fabricated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
