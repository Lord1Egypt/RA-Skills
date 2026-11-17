## Description:

Provides Chord market data and swap quotes across supported chains, and prepares unsigned EVM swap transactions for users to review and sign in their own wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuantqse90](https://clawhub.ai/user/tuantqse90)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet users, traders, and developers can review on-chain token prices, activity, stock-token data, and swap routes on supported EVM chains, as well as Solana market data. With explicit confirmation, they can prepare an unsigned EVM swap for their own wallet to sign.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chord receives wallet addresses, selected tokens, amounts, and quote or simulation details.

Mitigation: Share these details only if comfortable with Chord receiving them; never share a private key or seed phrase.

Risk: A mistaken token, approval, route, or minimum received could expose funds to loss when a user signs a transaction.

Mitigation: Before signing in the user's own wallet, check the chain, full token addresses, approval spender and amount, router, and minimum received.

Risk: Read-only backtests for perps, FX, and metals appear in the documentation despite the skill's stated perps exclusion.

Mitigation: Treat these backtests as read-only information, not as a capability to place leveraged trades or orders.

## Reference(s):

- [Chord documentation](https://getchord.xyz/docs)
- [Chord homepage](https://getchord.xyz)
- [Chord API reference](https://getchord.xyz/docs/openapi.json)
- [Chord skill on ClawHub](https://clawhub.ai/tuantqse90/skills/chord)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Unsigned transaction data]

**Output Format:** [Concise text or Markdown summaries, with transaction details when requested and confirmed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source and time for market data; swap transactions remain unsigned and require review and signing in the user's own wallet.]

## Skill Version(s):

1.1.4 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
