## Description:

Collect CoinGecko and DefiLlama marks or compare one with a Coinbase Exchange trade with exact IDs, provider timestamps, source hashes and explicit gaps; retrieve compatible daily price history. Use when preparing a sourced crypto market brief, comparing fresh prices or collecting evidence for a daily strategy experiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and researchers use this skill to collect timestamped, source-backed cryptocurrency price marks and daily history for market briefs or strategy experiments, with explicit data gaps and limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis is benign but medium confidence because part of a script was only partially inspected.

Mitigation: Consider that uncertainty before installing and review the skill's behavior before use.

Risk: Aggregate price marks or daily history could be mistaken for executable prices or independent market corroboration.

Mitigation: Keep aggregate marks distinct from venue quotes and balances, report timestamp alignment and source limitations, and do not base a position decision on a snapshot alone.

## Reference(s):

- [Request and output contract](references/requests.md)
- [Primary sources and verification](references/sources.md)
- [CoinGecko simple price](https://docs.coingecko.com/demo/reference/simple-price)
- [CoinGecko daily market history](https://docs.coingecko.com/demo/reference/coins-id-market-chart)
- [DefiLlama free endpoint reference](https://api-docs.defillama.com/llms-free.txt)
- [Coinbase Exchange product ticker](https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-ticker)
- [ClawHub skill page](https://clawhub.ai/galleonlabs/skills/galleon-defi-market-snapshot)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Markdown market brief with structured JSON observations or a daily history dataset]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes exact asset IDs, USD units, observation and retrieval timestamps, source hashes, and explicit gaps or limitations.]

## Skill Version(s):

0.8.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
