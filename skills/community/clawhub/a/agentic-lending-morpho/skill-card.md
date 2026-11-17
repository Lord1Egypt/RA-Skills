## Description:

Plans and executes guarded Morpho market workflows for Api3-backed lending markets, including explicit asset selection, oracle-route resolution, feed-readiness checks or funding, deployment, and verification when signer-backed execution is explicitly allowed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daav3](https://clawhub.ai/user/daav3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DeFi operators use this skill to plan, dry-run, or explicitly execute Morpho market and market-set workflows for selected collateral and borrow assets. It helps resolve Api3 oracle routes, classify or fund feeds when supported, deploy the Morpho oracle adapter and market, and report verification status without overstating incomplete runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw wallet keys can be accepted by the runtime and may be written into saved run artifacts.

Mitigation: Use environment-variable based signer inputs such as LIVE_SIGNER_ENV, never inline privateKey fields, keep request files free of secrets, and rotate any wallet whose real key was saved in an old run directory.

Risk: Signer-backed execution can create forward-only on-chain changes that cannot be undone by deleting local files.

Mitigation: Default to planning or dry-run, require explicit approval before transaction submission, inspect approval-summary.json before live execution, and inspect rollback-plan.json before any dependent transaction.

Risk: Bundled feed-status and market-registry data are packaged snapshots and may not reflect current on-chain state.

Mitigation: Use live RPC-backed feed checks for deployment or verification claims and treat packaged data as fallback planning input only.

Risk: Browser-assisted or unsupported feed funding branches can block an autonomous deployment path.

Mitigation: Report browser-assisted funding as a user handoff, stop on unsupported routes, and only continue to deployment after feed readiness and propagation are proven.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daav3/skills/agentic-lending-morpho)
- [Project Homepage](https://github.com/daav3/agentic-lending-project)
- [Workflow](references/workflow.md)
- [Current Capabilities and Limits](references/current_capabilities.md)
- [Morpho Oracle Adapter](references/morpho-oracle-adapter.md)
- [Feed-to-Market State Machine](references/state-machine.md)
- [Wrapper Summary Contract](references/summary-contract.md)
- [Live Request Template](references/live-request-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON request, approval, decision, rollback, progress, deployment, and verification artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local run directories and resumable artifacts; final success claims depend on explicit wrapper fields and on-chain verification evidence.]

## Skill Version(s):

0.1.11 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
