## Description:

Gets cryptocurrency token prices and generates candlestick charts using CoinGecko or Hyperliquid market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evgyur](https://clawhub.ai/user/evgyur)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to look up cryptocurrency token prices, recent percentage changes, and generated candlestick charts for supported CoinGecko or Hyperliquid assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token lookup requests are sent to CoinGecko and Hyperliquid.

Mitigation: Use the skill only when those public market-data API requests are acceptable for the user's environment.

Risk: Generated chart and cache files are written under /tmp.

Mitigation: On shared or multi-user hosts, use a hardened deployment with a private temp/cache directory.

Risk: The Python dependency is specified as a minimum version rather than pinned exactly.

Mitigation: Pin and review dependencies before deploying in controlled production environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evgyur/skills/crypto-price)
- [CoinGecko API](https://api.coingecko.com/api/v3/)
- [Hyperliquid Info API](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [JSON object containing price fields, text_plain, and chart_path for a generated PNG chart.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes short-lived price cache JSON files and generated chart PNG files under /tmp.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
