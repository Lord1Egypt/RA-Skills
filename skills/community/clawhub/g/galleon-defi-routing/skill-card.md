## Description:

Compares token swaps and cross-chain routes, prepares reviewed transaction handoffs, and tracks delivery, partial outcomes, and refunds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

People and agents comparing DeFi swap and bridge routes use this skill to review costs and transaction details, hand approved payloads to a trusted wallet, and reconcile destination delivery or refunds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect quote, spender, fee, recipient, or payload could lead to unintended financial loss.

Mitigation: Review exact route terms and costs before handoff; keep signing in the user's trusted wallet.

Risk: A source transaction or pending bridge status may be mistaken for successful destination delivery.

Mitigation: Reconcile original request IDs, destination receipts, actual assets and amounts, and refund state before reporting completion or retrying.

Risk: Overbroad tool, wallet, or API access could exceed the user's intended task.

Mitigation: Use only task-specific tools and permissions; do not provide API keys or wallet authority beyond the requested work.

## Reference(s):

- [Galleon DeFi Routing on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-defi-routing)
- [Provider access and requirements](artifact/references/providers.md)
- [Route and recovery workflows](artifact/references/workflows.md)
- [LI.FI status recovery](https://docs.li.fi/agents/workflows/status-recovery)
- [Circle CCTP technical guide](https://developers.circle.com/cctp/references/technical-guide)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Transaction handoff details]

**Output Format:** [Markdown text with route comparisons and settlement records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes route costs, quote validity, receipt status, and unresolved gaps when available; does not sign transactions.]

## Skill Version(s):

0.3.1 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
