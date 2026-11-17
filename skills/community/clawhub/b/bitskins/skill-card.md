## Description:

Interacts with the BitSkins REST API V2 and WebSocket API for CS2/Dota 2 skin trading, including account management, market search, buying, selling, wallet operations, Steam inventory, deposits, trades, and real-time marketplace subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluesyparty-src](https://clawhub.ai/user/bluesyparty-src)

### License/Terms of Use:


## Use Case:

Developers and trading-account operators use this skill to ask an agent for BitSkins API guidance, request shell commands, and prepare REST or WebSocket interactions for marketplace, inventory, wallet, and account workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A powerful BitSkins API key could leak credentials or enable high-impact account and financial actions if mishandled.

Mitigation: Use a tightly scoped API key, avoid exposing secrets in command history or process arguments, and revoke the key if exposure is suspected.

Risk: Purchases, sales, withdrawals, deposits, API-key changes, 2FA changes, and account-security operations can affect funds, inventory, or account access.

Mitigation: Require explicit user confirmation for each sensitive action and request fresh 2FA codes only when needed.

Risk: An unsafe request path could cause unintended API calls through the helper.

Mitigation: Validate request paths before execution and limit calls to expected BitSkins API endpoints.

## Reference(s):

- [BitSkins API endpoint reference](references/api-endpoints.md)
- [BitSkins WebSocket API](references/websocket.md)
- [BitSkins REST API base URL](https://api.bitskins.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BITSKINS_API_KEY; sensitive account, trading, wallet, API-key, and 2FA actions should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
