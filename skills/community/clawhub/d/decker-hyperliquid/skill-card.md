## Description:

Guides agents through Hyperliquid DEX price, position, and order workflows via Decker, with safety checks for order confirmation, position sizing, slippage, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigshow](https://clawhub.ai/user/gigshow)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to route Hyperliquid perpetual DEX trading requests through Decker in Slack or Telegram. It provides setup guidance for Hyperliquid API wallets, price and position checks, and user-confirmed order requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide Decker and Hyperliquid trading actions that may execute real financial orders.

Mitigation: Require explicit user confirmation of coin, side, size, price, estimated cost, current price, and existing positions before any order request.

Risk: Hyperliquid setup may involve giving Decker a trade-capable private key.

Mitigation: Use a dedicated low-risk API wallet, avoid putting secrets in URLs or logs, and confirm Decker key storage, revocation, replay protection, and order limits before use.

Risk: Market orders, large position sizes, or off-market limit prices can cause unintended trading outcomes.

Mitigation: Warn on large orders, compare limit prices to current market prices, disclose slippage assumptions, and do not retry failed orders without user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gigshow/skills/decker-hyperliquid)
- [Decker API base URL](https://api.decker-ai.com)
- [Hyperliquid API wallet setup](https://app.hyperliquid.xyz/API)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown with inline request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes trading safety checks and manual confirmation expectations.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
