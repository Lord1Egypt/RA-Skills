## Description:

Analyze Chinese stock prices (A-shares, HK stocks) and provide investment recommendations. Use when the user asks about stock analysis for Chinese companies, including buying/selling recommendations and market trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c595390153-a11y](https://clawhub.ai/user/c595390153-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request structured stock analysis for A-shares, Hong Kong stocks, and related Chinese companies, including price context, technical signals, and buy, hold, or sell guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Buy, hold, or sell recommendations may be mistaken for personalized financial advice.

Mitigation: Treat outputs as informational only and retain the skill's investment risk disclaimer.

Risk: Market data, news, and sentiment can become outdated or incomplete.

Mitigation: Verify current price, volume, and news context before relying on the analysis.

Risk: The skill is China-focused but may discuss U.S. stocks, and its templates default to Chinese.

Mitigation: Confirm the requested market and preferred language before using generated analysis.

## Reference(s):

- [Popular Chinese Stocks Reference](references/china-stocks.md)
- [Eastmoney](https://www.eastmoney.com)
- [Xueqiu](https://xueqiu.com)
- [Yahoo Finance](https://finance.yahoo.com)
- [Google Finance](https://www.google.com/finance)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown stock-analysis report with tables and recommendation bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Should include the standard investment risk disclaimer.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
