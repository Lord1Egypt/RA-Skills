## Description:

Analyze Chinese stock prices (A-shares, HK stocks) and provide investment recommendations when users ask about Chinese companies, buying or selling considerations, and market trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to ask an agent for structured stock analysis across Mainland China A-shares, Hong Kong listings, and related market examples. The skill guides the agent to gather current market data, summarize technical context, and present buy, hold, or sell considerations with a risk disclaimer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data or recommendations may be inaccurate, stale, or unsuitable for a user's financial situation.

Mitigation: Verify live prices, news, and fundamentals independently, and treat buy, hold, or sell output as informational rather than professional financial advice.

Risk: The skill can respond outside its primary China-stock focus and may default to Chinese-language formatting.

Mitigation: Confirm the target market, ticker, and desired language before relying on the analysis.

## Reference(s):

- [Common Chinese Stocks Reference](references/china-stocks.md)
- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/skills/chen-china-stock-analysis)
- [East Money](https://www.eastmoney.com)
- [Xueqiu](https://xueqiu.com)
- [Yahoo Finance](https://finance.yahoo.com)
- [Google Finance](https://www.google.com/finance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown stock analysis with tables, trend commentary, recommendation rationale, and a risk disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires independent verification of live market data; the skill directs the agent to include a standard investment-risk disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
