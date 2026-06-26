## Description: <br>
Query real-time cryptocurrency prices using the Binance API, including latest prices for Bitcoin, Ethereum, and Binance-listed cryptocurrencies without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangzhe1991](https://clawhub.ai/user/yangzhe1991) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to fetch public Binance spot-market prices for popular cryptocurrencies or a requested trading pair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Binance to fetch public market prices, so results depend on network access and Binance API availability. <br>
Mitigation: Use it only where outbound requests to Binance are acceptable, and treat returned prices as live market data rather than guaranteed execution prices. <br>
Risk: The script accepts a user-provided trading symbol. <br>
Mitigation: Avoid entering private or unrelated text as the symbol, matching the security guidance in evidence.json. <br>
Risk: The script depends on the Python requests package without a pinned exact version. <br>
Mitigation: Pin and review dependencies in stricter environments before deployment. <br>


## Reference(s): <br>
- [ClawHub Binance Crypto Price release page](https://clawhub.ai/yangzhe1991/binance-crypto-price) <br>
- [Binance Spot ticker price endpoint](https://api.binance.com/api/v3/ticker/price) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text price summaries or JSON objects printed by the script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; output depends on live Binance API availability and market data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
