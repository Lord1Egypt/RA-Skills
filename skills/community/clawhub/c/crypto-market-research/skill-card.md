## Description:

Researches public cryptocurrency markets, coins, exchanges, categories, global metrics, news, NFTs, token unlocks, and treasuries through CoinGecko via the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to collect public cryptocurrency market snapshots and compare assets, categories, exchanges, and global trends without placing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and the API key pass through Crawlora as an intermediary.

Mitigation: Use a dedicated Crawlora API key and do not send secrets or private wallet or account data as query values.

Risk: Fast-changing market data can be mistaken for current prices or financial advice.

Mitigation: Report retrieval time, quote currency, source, and filters; treat snapshots as informational rather than predictions or investment advice.

## Reference(s):

- [CoinGecko endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/crypto-market-research)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown research summaries and JSON market data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; include quote currency, retrieval time, source, and filters in summaries.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
