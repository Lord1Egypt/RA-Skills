## Description: <br>
BitoPro Spot is an exchange API wrapper for public market data and private spot trading, including tickers, order books, account balances, order placement, order cancellation, trade history, and withdrawals for BitoPro pairs including TWD markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitopro](https://clawhub.ai/user/bitopro) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and trading agents use this skill to query BitoPro spot market data and, with configured credentials and explicit confirmations, manage account, order, and withdrawal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place trades, cancel orders, and initiate withdrawals when private credentials are configured. <br>
Mitigation: Use scoped BitoPro API keys, preferably with withdrawals disabled, and require exact, fresh confirmation of the asset, pair, amount, destination, and action before any trade, cancellation, or withdrawal. <br>
Risk: Private workflows require sensitive credentials including an API key, API secret, and account email. <br>
Mitigation: Store credentials only in environment variables, mask displayed API keys, and never display any portion of the API secret. <br>
Risk: The security review flags under-scoped confirmations and insufficient risk warnings for live trading and withdrawal behavior. <br>
Mitigation: Review the skill before installation and test in a sandbox or dry-run setup before permitting live account actions. <br>


## Reference(s): <br>
- [BitoPro API Authentication](references/authentication.md) <br>
- [BitoPro API Endpoints Reference](references/endpoints.md) <br>
- [BitoPro API base URL](https://api.bitopro.com/v3) <br>
- [BitoPro withdrawal address management](https://www.bitopro.com/address) <br>
- [ClawHub skill page](https://clawhub.ai/bitopro/bitopro-skills-hub) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bitopro) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with API request details and JSON-shaped request or response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public market-data use needs no API key; private account, trading, cancellation, and withdrawal workflows require BitoPro credentials and explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter lists 2.5.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
