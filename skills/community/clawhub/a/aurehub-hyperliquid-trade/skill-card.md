## Description:

Trade on Hyperliquid for spot and perpetual futures with market orders, limit orders, leverage setting, WDK wallet support, and USDC deposits from Arbitrum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aure-duncan](https://clawhub.ai/user/aure-duncan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent check Hyperliquid balances, place spot and perpetual trades, manage limit orders, and bridge or withdraw USDC through configured wallet scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can decrypt a local wallet and sign trades, leverage changes, deposits, withdrawals, order cancellations, and order modifications.

Mitigation: Use a dedicated low-balance wallet, review previews carefully, keep confirmation thresholds conservative, and verify each financial action before approving execution.

Risk: Optional rankings registration can share a wallet address and nickname with xaue.com.

Mitigation: Decline rankings opt-in unless that disclosure is intended, and use a nickname that does not expose sensitive personal information.

Risk: Shared or untrusted local wallet and environment files can expose secrets or alter runtime behavior.

Mitigation: Keep ~/.aurehub files private, avoid shared configuration, and review ~/.aurehub/.env before use.

## Reference(s):

- [Balance](references/balance.md)
- [Limit Order](references/limit-order.md)
- [Onboarding](references/onboarding.md)
- [Perp Trade](references/perp-trade.md)
- [Spot Trade](references/spot-trade.md)
- [Wallet Modes](references/wallet-modes.md)
- [Hyperliquid](https://hyperliquid.xyz)
- [Hyperliquid App](https://app.hyperliquid.xyz)
- [Hyperliquid API Endpoint](https://api.hyperliquid.xyz)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local configuration, wallet state, and external Hyperliquid or Arbitrum API responses when executing user-approved flows.]

## Skill Version(s):

1.3.0 (source: server release metadata, skill metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
