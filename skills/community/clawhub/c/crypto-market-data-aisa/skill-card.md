## Description:

Query real-time and historical cryptocurrency market data through AIsa's CoinGecko API, including prices, charts, OHLC candles, token lookup, market-cap rankings, exchange data, categories, trending searches, and crypto news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch cryptocurrency market data, resolve coin and exchange identifiers, screen market-cap rankings, inspect token contract pricing, and gather current or historical CoinGecko-derived data for research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The top-level routing text overclaims support for stock and dividend workflows.

Mitigation: Use the skill only for cryptocurrency market data and route equities, dividends, and traditional finance requests to a dedicated traditional finance tool.

Risk: The skill requires AISA_API_KEY for API access.

Mitigation: Provide the key through the environment and keep it out of committed files, shared prompts, transcripts, and logs.

Risk: Market prices, rankings, news, and trending data can become stale or incomplete.

Mitigation: Check timestamps and corroborate important financial conclusions with authoritative sources before acting on them.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/baofeng-tech/skills/crypto-market-data-aisa)
- [AIsa](https://aisa.one)
- [AIsa API Reference](https://aisa.one/docs/api-reference)
- [AIsa CoinGecko Simple Price](https://aisa.one/docs/api-reference/coingecko/simple-price)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples; the CLI prints JSON market-data payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY. Outputs market data only and should not be treated as investment advice.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
