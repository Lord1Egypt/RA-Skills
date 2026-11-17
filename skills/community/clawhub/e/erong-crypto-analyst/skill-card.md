## Description:

Crypto Analyst provides cryptocurrency market analysis across OKX, Binance, and AKShare, including price queries, technical analysis, trading signals, fund-flow checks, position sizing, DCA planning, and risk calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erongcao](https://clawhub.ai/user/erongcao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather crypto market data, run technical analysis, compare exchange prices, track large trades, and produce trading-risk planning guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default OKX analysis can attempt to call hard-coded external news scripts.

Mitigation: Review those script calls before use or run OKX analysis with --no-news when the news integrations are not trusted or available.

Risk: OKX account workflows use API credentials for account-balance access.

Mitigation: Use read-only OKX keys with minimum account permissions, no withdrawal or trading permissions, and a dedicated environment.

Risk: The dependency list is not pinned.

Mitigation: Install dependencies in an isolated virtual environment and prefer pinned requirements before operational use.

## Reference(s):

- [Crypto Analyst on ClawHub](https://clawhub.ai/erongcao/skills/erong-crypto-analyst)
- [OKX API](https://www.okx.com)
- [Binance Market Data API](https://data-api.binance.vision)
- [Binance Futures API](https://fapi.binance.com)
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/)
- [NS3 Feed API](https://api.ns3.ai/feed)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and terminal text with tables, command examples, signal summaries, and risk guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external market-data services and optional OKX account endpoints when credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
