## Description:

Analyzes one BTC or ETH derivatives setup using public Deribit, Hyperliquid, and Polymarket data for read-only strategy research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frederica123](https://clawhub.ai/user/frederica123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect public BTC or ETH derivatives data, review volatility, skew, funding, basis, support and resistance, prediction-market context, and select a best-fit research strategy without executing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake strategy fit scores or market summaries for financial advice, win rates, expected returns, or profit guarantees.

Mitigation: Start delivered analysis with Not investment advice, preserve setup-fit scores as fit scores only, and avoid exact trade sizing, leverage, probabilities of profit, payoff ratios, or expected returns.

Risk: Public Deribit, Hyperliquid, and Polymarket data can be unavailable, delayed, venue-specific, or governed by contract-specific rules.

Mitigation: Review source availability, timestamps, prediction-market rules, and agreement between independent sources before using the analysis.

Risk: The skill installs a Python dependency and saves local research bundles or cards under the configured output directory.

Mitigation: Install in a dedicated virtual environment, pin and audit the mcp dependency, and review saved local files before sharing them.

Risk: Exchange credentials or account access would increase financial and security risk.

Mitigation: Use only public keyless endpoints and do not provide exchange credentials or connect the skill to an exchange account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frederica123/skills/crypto-market-strategist)
- [Deribit public API](https://www.deribit.com/api/v2/public)
- [Hyperliquid public Info API](https://api.hyperliquid.xyz/info)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown analysis with JSON strategy inputs and saved local JSON research bundles or strategy cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; limited to one selected asset, BTC or ETH; delivered analysis starts with Not investment advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
