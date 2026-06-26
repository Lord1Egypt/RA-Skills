## Description: <br>
Provides Binance API integration for spot and futures trading, including balances, market data, order management, leverage settings, and position management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ly5201314gjx](https://clawhub.ai/user/ly5201314gjx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Binance account and market data and to execute spot and futures trading actions through configured Binance API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can place spot and futures orders, change leverage, and close positions against a live Binance account. <br>
Mitigation: Use a separate restricted API key with withdrawals disabled, test first with testnet or very small limits, and require explicit human confirmation before trades, leverage changes, or position closes. <br>
Risk: Credential exposure or misuse could allow unauthorized account access. <br>
Mitigation: Provide BINANCE_API_KEY and BINANCE_SECRET_KEY only through environment variables or a managed secret store, never hardcode them, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ly5201314gjx/binance-skill-export) <br>
- [Binance Spot API endpoint](https://api.binance.com) <br>
- [Binance Futures API endpoint](https://fapi.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, JSON, configuration, guidance] <br>
**Output Format:** [Text responses with structured details objects from Binance API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BINANCE_API_KEY and BINANCE_SECRET_KEY environment variables for authenticated account and trading operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
