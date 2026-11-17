## Description:

Collects sourced crypto price snapshots and validated daily history from public CoinGecko and DefiLlama data, with timestamps, source hashes and explicit gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to prepare cited crypto market briefs, compare fresh price observations and collect daily price history for research. Aggregate marks are not executable quotes or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public price requests disclose the requested asset IDs to CoinGecko and DefiLlama.

Mitigation: Use the skill only when public, keyless requests for those IDs are acceptable.

Risk: Aggregate prices or stale and incomplete observations could be mistaken for executable quotes or investment advice.

Mitigation: Review timestamps and gaps; use official provider or venue tools for consequential financial decisions.

## Reference(s):

- [Request and output contract](artifact/references/requests.md)
- [Primary sources and verification](artifact/references/sources.md)
- [CoinGecko simple price documentation](https://docs.coingecko.com/demo/reference/simple-price)
- [CoinGecko market-chart documentation](https://docs.coingecko.com/demo/reference/coins-id-market-chart)
- [DefiLlama free API reference](https://api-docs.defillama.com/llms-free.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Sourced market brief in Markdown and structured JSON price or history data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes exact asset IDs, USD units, observation and retrieval times, source hashes, and explicit missing or stale data.]

## Skill Version(s):

0.6.1 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
