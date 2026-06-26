## Description: <br>
Retrieves real-time USD prices for major cryptocurrencies such as Bitcoin and Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer cryptocurrency price questions by fetching a requested symbol's current USDT price and 24-hour percentage change. It defaults to BTC when no symbol is supplied and returns clear messages for unavailable coins or exchange API failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound network requests to Binance through ccxt to retrieve market data. <br>
Mitigation: Install only in environments where outbound exchange requests are allowed and ensure the runtime has ccxt available. <br>
Risk: Returned cryptocurrency prices may be unavailable, delayed, or unsuitable for financial decisions. <br>
Mitigation: Treat responses as informational, verify important prices independently, and do not use them as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robertstarry-gif/crypto-price-by-lpdawn-bak) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text price response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the requested symbol, current USDT price, and 24-hour percentage change, or a clear error message.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
