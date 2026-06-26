## Description: <br>
Monitor live cryptocurrency prices, technical indicators, support and resistance levels, and configurable price alerts using public CoinGecko market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to fetch current cryptocurrency market data, compute simple technical indicators, and generate informational price alerts or portfolio summaries. It is intended for market monitoring, not financial advice or automated trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data and simple technical indicators may be mistaken for financial advice or trading instructions. <br>
Mitigation: Use the skill only as an informational market-data helper and require human review before any portfolio or trading decision. <br>
Risk: Generic trigger terms or common crypto symbols may activate the skill more broadly than intended. <br>
Mitigation: Confirm the user is asking for cryptocurrency price, alert, or analysis help before running the price-check workflow. <br>
Risk: Future changes that add wallet keys, exchange credentials, or trading permissions would materially change the security profile. <br>
Mitigation: Do not add credentials or trading capabilities without a separate security review. <br>
Risk: Live results depend on public CoinGecko API availability, freshness, and rate limits. <br>
Mitigation: Surface API errors clearly, preserve timestamps in results, and avoid treating stale or failed fetches as authoritative. <br>


## Reference(s): <br>
- [Technical Signals Reference](references/signals.md) <br>
- [CoinGecko Search API endpoint](https://api.coingecko.com/api/v3/search) <br>
- [CoinGecko Simple Price API endpoint](https://api.coingecko.com/api/v3/simple/price) <br>
- [CoinGecko Coins API endpoint](https://api.coingecko.com/api/v3/coins) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text report or JSON object, with optional shell command examples for running the price checker.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public CoinGecko API data, requires no credentials, and includes timestamps on fetched market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
