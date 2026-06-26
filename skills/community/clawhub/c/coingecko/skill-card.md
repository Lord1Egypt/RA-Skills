## Description: <br>
Fetch crypto prices, market data, and token info from the CoinGecko free API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olisim02](https://clawhub.ai/user/olisim02) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve CoinGecko cryptocurrency prices, market caps, 24-hour changes, trending coins, and token details by coin ID, ticker search, or contract address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered crypto queries and token contract addresses are sent to CoinGecko. <br>
Mitigation: Do not submit sensitive private identifiers, and review whether external API requests are acceptable for the deployment environment. <br>
Risk: Returned crypto market data may be delayed, incomplete, unavailable, or unsuitable for financial decision-making. <br>
Mitigation: Treat results as informational and verify important market data against authoritative sources before acting on it. <br>
Risk: Bulk lookups can encounter CoinGecko public API rate limits. <br>
Mitigation: Cache results where practical and avoid tight request loops. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/olisim02/coingecko) <br>
- [CoinGecko markets endpoint used by price.py](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h,7d) <br>
- [CoinGecko search endpoint used by search.py](https://api.coingecko.com/api/v3/search?query={query}) <br>
- [CoinGecko contract endpoint used by token.py](https://api.coingecko.com/api/v3/coins/{platform}/contract/{address}) <br>
- [CoinGecko trending endpoint used by trending.py](https://api.coingecko.com/api/v3/search/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on network access, CoinGecko API availability, and public API rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
