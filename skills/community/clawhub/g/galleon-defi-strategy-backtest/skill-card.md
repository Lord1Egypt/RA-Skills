## Description:

Tests daily long-only buy-and-hold, funded DCA, or moving-average crypto strategies against local historical data with costs, cash flows, drawdown, and a benchmark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and crypto researchers use this skill to evaluate a predefined daily spot strategy on dated local data, compare it with buy-and-hold, and inspect held-out results and cost sensitivity before considering any trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Historical or synthetic returns may be mistaken for realistic future trading performance.

Mitigation: Treat results as research only; identify synthetic versus market data, disclose model limits, and verify venue fills and assumptions independently before acting.

Risk: Untrusted market data or disclosed private holdings may distort results or expose sensitive account information.

Mitigation: Use trusted local datasets, check data identity and dates, and keep private holdings and account mappings out of shared reports.

Risk: External market-data collection may require separate provider access and verification.

Mitigation: Independently verify any CoinGecko or venue data-collection workflow; the bundled backtest reads local files and does not execute trades.

## Reference(s):

- [Input and accounting contract](references/model.md)
- [Data and research workflow](references/research.md)
- [CoinGecko market-chart documentation](https://docs.coingecko.com/demo/reference/coins-id-market-chart)

## Skill Output:

**Output Type(s):** [Analysis, JSON reports, Guidance]

**Output Format:** [JSON backtest reports and human-readable research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include dated trades, an equity curve, input hashes, drawdown, a same-cost benchmark, and independent held-out and higher-cost comparisons.]

## Skill Version(s):

0.2.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
