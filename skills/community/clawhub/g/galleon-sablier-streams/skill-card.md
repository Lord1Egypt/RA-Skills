## Description:

Use when creating, funding, withdrawing, pausing or cancelling Sablier Flow streams or Lockup vesting, or diagnosing covered versus uncovered stream debt. Resolve product, deployment and current NFT rights before preparing a bounded payment action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and payment operators use the skill to interpret Sablier Flow and Lockup stream state, calculate obligations, and prepare bounded create, fund, withdraw, pause, or cancellation actions. It helps agents report current rights, covered debt or vesting, and the evidence needed to reconcile a payment action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review found one unresolved local reference in SKILL.md, so the available evidence is incomplete.

Mitigation: Check the cited module procedure against current official Sablier documentation and the exact chain deployment before preparing a payment action.

## Reference(s):

- [Sablier Flow overview](https://docs.sablier.com/concepts/flow/overview)
- [Flow deployments](https://docs.sablier.com/guides/flow/deployments)
- [Sablier cancelability](https://docs.sablier.com/concepts/cancelability)
- [Official Flow creation procedure](https://github.com/sablier-labs/sablier-skills/blob/main/skills/sablier-create-open-ended-stream/references/evm-onchain.md)
- [Official Flow cancellation procedure](https://github.com/sablier-labs/sablier-skills/blob/main/skills/sablier-cancel-open-ended-stream/references/cli.md)
- [Official Lockup creation procedure](https://github.com/sablier-labs/sablier-skills/blob/main/skills/sablier-create-vesting/references/evm-onchain.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, API Calls, Markdown]

**Output Format:** [Markdown decision record with stream state, obligation calculations, and reviewed unsigned calls or transaction receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded to the requested stream action and supported by observed product, deployment, rights, and payment evidence.]

## Skill Version(s):

0.3.0 (source: evidence release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
