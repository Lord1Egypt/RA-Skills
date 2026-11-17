## Description:

Query GeckoTerminal market data - networks, DEXes, pools, tokens, OHLCV, trades, and trending/new pools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brs999](https://clawhub.ai/user/brs999)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to query public GeckoTerminal market data for network, DEX, pool, token, OHLCV, trade, trending, and new-pool analysis without wallet or trading access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data searches, token addresses, pool addresses, and query parameters are sent to GeckoTerminal.

Mitigation: Use the skill for public market-data lookups only and avoid submitting sensitive strategy, portfolio, or private research details as query text.

Risk: Users may over-rely on returned market data for trading or transaction decisions.

Mitigation: Treat outputs as informational market data, verify important results independently, and do not use the skill as a trading, wallet, or transaction tool.

Risk: Outbound API availability, latency, or upstream response changes can affect CLI results.

Mitigation: Handle failed or unexpected responses before relying on the output in automated briefs, dashboards, or downstream analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brs999/skills/gecko-terminal)
- [GeckoTerminal](https://www.geckoterminal.com)
- [GeckoTerminal API v2](https://api.geckoterminal.com/api/v2)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [JSON API responses with concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default CLI output is JSON for piping and automation; requests are read-only HTTPS GET calls to GeckoTerminal public API v2.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
