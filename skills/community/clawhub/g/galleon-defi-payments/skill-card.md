## Description:

Helps plan and reconcile stablecoin transfers, paid x402 requests, token streams, vesting and airdrop distribution using official wallet and protocol tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to scope payment obligations, prepare bounded transactions and reconcile payment, settlement and service delivery without treating a request as authorization to spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mistaken asset, chain, recipient or amount can cause unintended spending.

Mitigation: Require exact chain, asset, recipient and amount limits; review transaction and paid-request terms before signing.

Risk: Wallet secrets or signatures may be exposed through chat or logs.

Mitigation: Keep wallet secrets and raw signatures outside chat and artifacts; use trusted wallet and provider controls.

Risk: A timeout or accepted payment can be mistaken for failure or final settlement, causing duplicate payment or incorrect reconciliation.

Mitigation: Check the existing payment identity and receipts before retrying; report authorization, settlement and delivery separately.

## Reference(s):

- [ClawHub release](https://clawhub.ai/galleonlabs/skills/galleon-defi-payments)
- [Official payment providers](references/providers.md)
- [Payment workflows](references/workflows.md)
- [x402 v2 verification and recovery](references/x402-v2.md)
- [x402 HTTP payment contract](https://docs.x402.org/core-concepts/http-402)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown plan or payment receipt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authorized limits, observed payment state, fees, delivery status and unresolved next steps.]

## Skill Version(s):

0.2.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
