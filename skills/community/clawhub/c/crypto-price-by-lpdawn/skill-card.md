## Description: <br>
Fetches real-time USD prices for major cryptocurrencies such as Bitcoin and Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LPDawn](https://clawhub.ai/user/LPDawn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer current cryptocurrency price questions by querying a requested symbol such as BTC, ETH, DOGE, SOL, or LTC. If no symbol is supplied, the skill defaults to BTC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Binance through ccxt and depends on exchange availability and the ccxt package available in the runtime environment. <br>
Mitigation: Use it for simple public price checks, handle exchange failures gracefully, and separately pin or review runtime dependencies before deployment. <br>
Risk: Cryptocurrency price responses may be mistaken for trading or financial advice. <br>
Mitigation: Present results as informational market data only and do not grant wallet, exchange-account, or trading permissions without a separate review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LPDawn/crypto-price-by-lpdawn) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, shell commands, guidance] <br>
**Output Format:** [Plain text price response with current USDT price and 24-hour percentage change] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a cryptocurrency symbol input and returns an error message when the symbol or exchange request cannot be resolved.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
