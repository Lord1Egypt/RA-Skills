## Description:

Analyze Chinese stock prices (A-shares, HK stocks) and provide investment recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather public market data, summarize price movement, technical context, recent news, and produce structured buy, hold, or sell commentary for Chinese A-shares, Hong Kong stocks, and supported US stocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce explicit buy, hold, or sell suggestions that may be mistaken for personalized financial advice.

Mitigation: Present the output as educational market commentary, include the required risk disclaimer, and have users consult qualified financial professionals before making investment decisions.

Risk: Market prices and news can change quickly, making stale or incomplete public data misleading.

Mitigation: Use current market data sources during analysis and state when data is unavailable, delayed, or uncertain.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/make453/skills/china-stock-analysis-bak)
- [Popular Chinese Stocks Reference](references/china-stocks.md)
- [Eastmoney](https://www.eastmoney.com)
- [Xueqiu](https://xueqiu.com)
- [Yahoo Finance](https://finance.yahoo.com)
- [Google Finance](https://www.google.com/finance)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown stock-analysis report with tables, bullets, and a risk disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public market data and news context when available; outputs should be treated as educational analysis, not personalized financial advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
