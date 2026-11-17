## Description:

Generate structured crypto market morning briefings from public crypto market and news sources, including market overview, key asset trends, macro and regulatory updates, risk warnings, and information sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce a concise morning briefing on cryptocurrency market conditions, major asset movements, macro and regulatory news, risk notes, and cited public sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto market briefings may be mistaken for investment advice or relied on without checking source freshness.

Mitigation: Treat the output as informational only and verify market, regulatory, and news items against primary sources before making financial decisions.

Risk: The skill makes outbound requests to public CoinGecko and CryptoPanic services and may fail or return delayed data when those services are unavailable or rate limited.

Mitigation: Run it only in environments where those external requests are permitted, and communicate that public market data may lag or be incomplete.

Risk: The release expects curl and jq, and install metadata includes a system package installation command.

Mitigation: Review dependency installation in the target environment and prefer managed base images or preinstalled dependencies where package-manager changes are restricted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/crypto-morning-briefing)
- [CoinGecko global crypto market API](https://api.coingecko.com/api/v3/global)
- [CoinGecko coin markets API](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,binancecoin&order=market_cap_desc&per_page=4&page=1&sparkline=false)
- [CryptoPanic public news RSS](https://cryptopanic.com/news/rss/)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown-style text briefing by default, or JSON when run with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language briefing; no API key required; requires curl and jq; uses public CoinGecko and CryptoPanic endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
