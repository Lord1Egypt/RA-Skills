## Description: <br>
BitMart Web3 Wallet skill lets agents query public token, chain, market, smart money, wallet balance, recent transaction, swap quote, and batch price data across supported chains without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mccoysc](https://clawhub.ai/user/mccoysc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to answer BitMart Web3 market and wallet questions, including token discovery, prices, smart money rankings, wallet balances, recent transactions, and swap quote estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses and token queries may be sent to BitMart APIs. <br>
Mitigation: Avoid querying wallet addresses or token searches that should not be associated with requests to BitMart. <br>
Risk: Swap quotes and market data can be mistaken for trade execution or financial advice. <br>
Mitigation: Treat returned quotes and market data as informational only and require separate user review before any trading action. <br>
Risk: The public API may rate limit requests or return unavailable quotes for unsupported token pairs or low-liquidity markets. <br>
Mitigation: Respect the documented 15 requests per second per IP limit and tell users when data or quotes are unavailable instead of fabricating results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mccoysc/bitmart-wallet-skill) <br>
- [BitMart homepage](https://www.bitmart.com) <br>
- [BitMart public API base URL](https://api-cloud.bitmart.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Guidance] <br>
**Output Format:** [Markdown or text responses grounded in JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public POST requests to BitMart APIs; no API key required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
