## Description:

Fetch crypto prices, market data, and token info from the CoinGecko free API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olisim02](https://clawhub.ai/user/olisim02)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up cryptocurrency prices, market metrics, trending coins, and token details by CoinGecko coin ID, ticker search, or supported contract address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto search terms and token addresses are sent to CoinGecko.

Mitigation: Avoid submitting sensitive or proprietary wallet, token, or investigation details unless disclosure to CoinGecko is acceptable.

Risk: Market data can change quickly and API responses may be delayed, unavailable, or rate limited.

Mitigation: Use results as market lookup data, cache bulk lookups, avoid tight loops, and verify high-impact financial decisions against authoritative sources.

## Reference(s):

- [ClawHub CoinGecko skill page](https://clawhub.ai/olisim02/skills/coingecko)
- [CoinGecko markets API endpoint](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h,7d)
- [CoinGecko search API endpoint](https://api.coingecko.com/api/v3/search?query={query})
- [CoinGecko contract lookup API endpoint](https://api.coingecko.com/api/v3/coins/{platform}/contract/{address})
- [CoinGecko trending API endpoint](https://api.coingecko.com/api/v3/search/trending)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CoinGecko results are real-time market data returned from public API calls.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
