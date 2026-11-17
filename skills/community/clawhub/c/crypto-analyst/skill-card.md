## Description:

Crypto Analyst helps agents gather cryptocurrency market data from OKX and Binance, run technical and sentiment analysis, compare exchanges, size positions, plan DCA purchases, and summarize risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erongcao](https://clawhub.ai/user/erongcao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce informational cryptocurrency market reports, trading-signal summaries, exchange comparisons, DCA plans, and position-sizing calculations from exchange and sentiment data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run unbundled local helper scripts when fetching news.

Mitigation: Review and trust those helper scripts before use, or run okx_analyst.py with --no-news.

Risk: The skill reads OKX exchange credentials from environment or .env files.

Mitigation: Use read-only OKX API keys with no trading or withdrawal permissions, and avoid placing broad credentials in the project .env.

Risk: Market signals, DCA plans, and position-sizing outputs can be incomplete or misleading if upstream market data is unavailable or volatile.

Mitigation: Treat outputs as informational analysis and independently review market data, assumptions, and risk limits before acting.

## Reference(s):

- [Crypto Analyst on ClawHub](https://clawhub.ai/erongcao/skills/crypto-analyst)
- [Publisher profile: erongcao](https://clawhub.ai/user/erongcao)
- [OKX API](https://www.okx.com)
- [Binance public market data](https://data-api.binance.vision)
- [Binance US API](https://api.binance.us)
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market prices, technical indicators, trading-signal summaries, DCA schedules, position-sizing calculations, account-balance summaries, and risk notes.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
