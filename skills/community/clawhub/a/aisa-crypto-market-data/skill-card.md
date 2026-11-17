## Description:

Provides an AIsa-backed CoinGecko command-line client for cryptocurrency prices, markets, coins, exchanges, news, and trending data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve cryptocurrency market data, including prices, markets, coin details, exchange data, news, and trending searches through the AIsa API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect broad web research because the skill text says web, multi-source, and last-30-days research, but the security summary identifies the shipped implementation as a read-only crypto market-data client.

Mitigation: Use it for crypto market-data queries unless the publisher clarifies broader retrieval support; do not claim sources that were not queried and report provider timeouts honestly.

Risk: Crypto market queries and AISA_API_KEY are sent to the AIsa API endpoint.

Mitigation: Install only where sending those queries and that credential to AIsa is acceptable, and scope or rotate the API key according to local policy.

## Reference(s):

- [AIsa homepage](https://aisa.one)
- [AIsa API endpoint](https://api.aisa.one/apis/v1)
- [ClawHub release page](https://clawhub.ai/baofeng-tech/skills/aisa-crypto-market-data)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands; CLI commands return pretty-printed JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; API requests are sent to AIsa.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
