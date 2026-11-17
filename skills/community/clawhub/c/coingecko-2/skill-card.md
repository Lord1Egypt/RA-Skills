## Description:

Live Bitcoin and crypto price data via CoinGecko API, including BTC/USD, ETH/USD, and multi-asset quotes with Demo or Pro API keys kept in environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bronoman](https://clawhub.ai/user/bronoman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve live cryptocurrency price and health-check data for monitoring, dashboards, alerts, and workflows that need current market context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling is under-scoped: evidence warns about a generic API_KEY fallback, documented key-revealing commands, and a published CG-looking key.

Mitigation: Use a dedicated CG_API_KEY, keep unrelated API_KEY values out of the working .env, remove or rotate any exposed key, and avoid commands that print secrets.

Risk: The multi-asset script may fail at runtime because it imports get_coingecko_api_key from fetch_price.py, where that function is not defined in the artifact.

Mitigation: Align the helper import or implement the missing function, then run health_check.py and fetch_multi_asset.py before deployment.

Risk: External market data can be rate-limited, unavailable, stale, or limited by fallback coverage.

Mitigation: Handle unsuccessful responses and source fields explicitly, verify prices independently for financial decisions, and expect Kraken fallback to cover fewer assets than CoinGecko.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/bronoman/hermes/tree/main/skills/coingecko)
- [ClawHub skill page](https://clawhub.ai/bronoman/skills/coingecko-2)
- [CoinGecko API documentation](https://www.coingecko.com/en/api/documentation)
- [CoinGecko API pricing](https://www.coingecko.com/en/api/pricing)
- [Kraken public ticker API](https://api.kraken.com/0/public/Ticker)
- [Technical reference](references/DESCRIPTION.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns current price, 24-hour change, market-cap, volume, bid/ask, source, status, and error fields depending on the script and upstream API response.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
