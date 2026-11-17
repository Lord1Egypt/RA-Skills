## Description:

Crypto Market Intelligence provides an OpenClaw agent with free public market data for crypto prices, market metrics, Fear & Greed index, DeFi TVL, stock indices, and macro indicators without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avmw2025](https://clawhub.ai/user/avmw2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to fetch current crypto, stock, and macro market data, then prepare concise market-intelligence summaries or trading-analysis prompts. It is suited for portfolio monitoring, market sentiment checks, and agent workflows that need fresh public market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public market-data APIs.

Mitigation: Install it only where agents are allowed to contact public market-data services, and review network access policies before use.

Risk: The skill writes fetched market data to local JSON files.

Mitigation: Choose an appropriate output directory and review file permissions for stored market data.

Risk: The cron example can create recurring background network activity.

Mitigation: Enable scheduling only when recurring fetches are intended, and document how to remove or adjust the cron entry.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/avmw2025/skills/crypto-market-intel)
- [Market Data API Sources](references/api-sources.md)
- [CoinGecko API Documentation](https://www.coingecko.com/en/api/documentation)
- [Alternative.me Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/)
- [DeFi Llama API Documentation](https://defillama.com/docs/api)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON market-data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes crypto-latest.json and stocks-latest.json to the selected local output directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
