## Description:

Explores and analyzes Api3 data feeds using public data by listing provider coverage, showing aggregation composition, fetching latest prices, comparing provider deviations, checking on-chain freshness, and cross-checking exchange spot prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api3dao](https://clawhub.ai/user/api3dao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and protocol operators use this skill to inspect Api3 dAPI provider coverage, aggregation participants, current feed values, stale timestamps, and divergence from public exchange spot prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public outbound requests may expose queried feed names, chain aliases, and asset pairs to Api3, RPC providers, and exchange APIs.

Mitigation: Install and run the skill only in environments where those public requests are acceptable, and avoid using sensitive or confidential query patterns.

Risk: Unpinned or non-repeatable dependency installation can change script behavior between installs.

Mitigation: Pin dependencies and use a lockfile before production or repeated operational use.

Risk: Feed health conclusions can be misleading if data is stale, provider coverage is sparse, or exchange spot references differ from the feed's source of truth.

Mitigation: Run the scripts fresh for each question, report UTC timestamps and data age, flag sparse aggregation or stale providers, and treat exchange composites as sanity checks rather than authoritative feed values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/api3dao/skills/api3-data-feed-explorer)
- [Api3 Signed API Public Endpoint](https://signed-api.api3.org/public/0xBA910Eb2867977A0a651FE3D2607237ff4116B1C)
- [Binance Ticker Price API](https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT)
- [Coinbase Spot Price API](https://api.coinbase.com/v2/prices/BTC-USD/spot)
- [Kraken Ticker API](https://api.kraken.com/0/public/Ticker?pair=XBTUSD)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with shell command snippets and tabular analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports UTC timestamps, provider values, freshness, deviations, and concise health guidance from fresh public-data queries.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
