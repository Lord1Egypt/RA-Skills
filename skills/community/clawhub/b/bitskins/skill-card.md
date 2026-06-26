## Description: <br>
Interacts with the BitSkins REST API V2 and WebSocket API for CS2 and Dota 2 skin trading, including account management, market search, buying, selling, listing, wallet operations, Steam inventory actions, and real-time marketplace subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluesyparty-src](https://clawhub.ai/user/bluesyparty-src) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill when they want an agent to search BitSkins markets, inspect prices and balances, manage listed items, or prepare API calls for BitSkins account and marketplace workflows. The skill should be used only by users who intentionally want an agent to operate their BitSkins account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real financial, marketplace, wallet, and account-security actions through BitSkins API calls. <br>
Mitigation: Require explicit user confirmation with the exact endpoint, item, amount, destination, and account-security impact before any buy, sell, deposit, withdrawal, API-key, 2FA, trade-link, card, or account-status change. <br>
Risk: The skill depends on a BitSkins API key that can authorize account actions. <br>
Mitigation: Keep the API key in the environment, avoid storing or displaying it, and use the narrowest BitSkins API permissions available. <br>


## Reference(s): <br>
- [BitSkins API V2 Endpoint Reference](references/api-endpoints.md) <br>
- [BitSkins WebSocket API](references/websocket.md) <br>
- [BitSkins API Base URL](https://api.bitskins.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON request bodies or API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BITSKINS_API_KEY in the environment and fresh 2FA codes for sensitive account, wallet, or security actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
