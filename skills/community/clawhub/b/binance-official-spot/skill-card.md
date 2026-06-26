## Description: <br>
Binance Spot request using the Binance API. Authentication requires API key and secret key. Supports testnet and mainnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viktor-huang](https://clawhub.ai/user/viktor-huang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and trading-operations users can use this skill to query Binance Spot market, account, and order endpoints, including authenticated requests that may place, amend, query, or cancel spot orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated endpoints can perform live financial actions, including order placement, amendment, cancellation, and account queries. <br>
Mitigation: Use testnet first and require explicit confirmation of account, endpoint, symbol, side, quantity, price, and action before any live order or cancellation. <br>
Risk: Binance API keys and secret keys can expose account data or trading authority if stored or shared unsafely. <br>
Mitigation: Use least-privilege keys with withdrawals disabled and IP restrictions, and avoid storing secrets in TOOLS.md, chat files, or other persistent agent-readable text. <br>
Risk: Ambiguous live-account defaults can route requests to mainnet when the user intended testnet. <br>
Mitigation: Set and confirm the target base URL and account environment before authenticated calls, especially before trading actions. <br>


## Reference(s): <br>
- [Authentication](references/authentication.md) <br>
- [ClawHub release page](https://clawhub.ai/viktor-huang/binance-official-spot) <br>
- [Binance Spot API mainnet](https://api.binance.com) <br>
- [Binance Spot testnet](https://testnet.binance.vision) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses with Markdown guidance and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated endpoints require signed Binance Spot requests with API key and secret key; the artifact documents both testnet and mainnet base URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
