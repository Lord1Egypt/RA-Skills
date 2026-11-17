## Description:

Read-only Morpho-first agentic lending planning for Api3-backed markets, including market-set exploration, oracle route resolution, feed readiness checks, and deployment or verification planning without signer-backed execution, funding, broadcast, or transaction submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daav3](https://clawhub.ai/user/daav3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan Morpho markets or market sets for selected collateral and borrow assets, resolve Api3-backed oracle paths, classify feed readiness, and prepare read-only deployment or verification handoffs. It is intended for planning and operator handoff only, not live funding or transaction execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake planning or dry-run analysis for completed Morpho deployment or verified on-chain state.

Mitigation: Label planning-only, operator handoff, and read-only verification states separately, and require a usable RPC endpoint before claiming on-chain verification.

Risk: Signer material, funding, deployment, or transaction submission could be pulled into a workflow that is designed to remain read-only.

Mitigation: Keep private keys and signer material out of scope, do not execute funding or broadcasts, and hand off any transaction step for separate operator review.

Risk: Unsupported oracle routes or unclear Api3 feed funding posture can block a Morpho market handoff.

Mitigation: Resolve direct or composed oracle routes explicitly, classify feed readiness as live, operator-fundable, browser-assisted, or unsupported, and report blockers before deployment planning.

## Reference(s):

- [Current capabilities and limits](references/current_capabilities.md)
- [Morpho oracle adapter, Api3-backed](references/morpho-oracle-adapter.md)
- [Morpho-first workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured planning status and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only planning output; funding, deployment, signer handling, broadcast, and transaction submission are out of scope.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
