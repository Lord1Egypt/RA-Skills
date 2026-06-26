## Description: <br>
Coinw Spot REST API skill for market data, order placement and cancellation, order queries, account balances, and asset transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[connectcoinw](https://clawhub.ai/user/connectcoinw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to connect an agent to CoinW spot trading APIs for market lookups, order management, balance checks, and spot-to-funding asset transfers. Private actions require CoinW API credentials and should be confirmed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place orders, cancel orders, cancel all open orders, view balances, and transfer assets, giving an agent high-impact account authority. <br>
Mitigation: Use a dedicated least-privilege CoinW API key and require explicit user confirmation before every order, cancellation, cancel-all, or transfer action. <br>
Risk: CoinW API keys and signed request data can expose sensitive account access if pasted into chat, logs, or support requests. <br>
Mitigation: Store credentials only in the configured secret mechanism, avoid pasting secrets into chat, and redact signed commands, request URLs, and logs before sharing. <br>
Risk: Overly broad API permissions can expand account exposure beyond the intended spot-trading workflow. <br>
Mitigation: Disable withdrawal or transfer permissions unless required, enable IP whitelisting where possible, and review the key permissions before installing the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/connectcoinw/coinw-spot-skill) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/connectcoinw) <br>
- [Authentication](references/Authentication.md) <br>
- [API Key Creation Steps](references/api-key-creation-steps.md) <br>
- [Error Code Explanation](references/error-codes.md) <br>
- [CoinW API Notes](references/notes.md) <br>
- [CoinW Get Trading Pair Information](https://www.coinw.com/api-doc/spot-trading/market/get-trading-pair-information) <br>
- [CoinW Place Order](https://www.coinw.com/api-doc/spot-trading/trade/place-order) <br>
- [CoinW Cancel All Orders](https://www.coinw.com/api-doc/spot-trading/trade/cancel-all-orders) <br>
- [CoinW Get Spot Account Balance](https://www.coinw.com/api-doc/spot-trading/account/get-spot-account-balance) <br>
- [CoinW Transfer Assets](https://www.coinw.com/api-doc/spot-trading/account/transfer-assets) <br>
- [CoinW Risk Disclosure Statement](https://www.coinw.com/help-center/announcement-center/product-updates/productupdates/2022-11-13/risk-disclosure-statement/2560) <br>
- [CoinW User Agreement](https://www.coinw.com/help-center/faq/official-updates/2020-04-15/user-agreement/6912) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, REST endpoint details, and credential setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COINW_API_KEY and COINW_SECRET_KEY for private endpoints; public market-data endpoints can be used without credentials.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
