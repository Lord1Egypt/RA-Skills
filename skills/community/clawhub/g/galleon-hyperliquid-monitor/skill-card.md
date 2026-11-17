## Description:

Reconciles current Hyperliquid account activity and risk, and reports watch conditions without placing or changing orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Traders, operators, and developers use this read-only skill to reconcile a specified public Hyperliquid account's positions, orders, fills, funding, and protection, or to assess a watch condition against fresh exchange data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stale, partial, or disconnected exchange data could misrepresent exposure or protection.

Mitigation: Require fresh account and order reconciliation; report missing or gapped evidence as unavailable rather than a healthy state.

Risk: Sharing signer secrets or installing unreviewed integrations can expose account access.

Mitigation: Provide only a public account address, never private keys or seed phrases, and pin reviewed versions for optional integrations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/galleonlabs/skills/galleon-hyperliquid-monitor)
- [Hyperliquid Info endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- [Authoritative state](references/authoritative-state.md)
- [Monitor output contract](references/output-contract.md)
- [Stream discipline](references/stream-discipline.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with account and order tables, timestamps, condition status, and evidence gaps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; reports triggered, not-triggered, unavailable, or incident states without submitting exchange actions.]

## Skill Version(s):

0.4.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
