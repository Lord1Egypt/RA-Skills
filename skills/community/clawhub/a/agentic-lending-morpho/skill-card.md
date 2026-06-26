## Description: <br>
Plan and execute the Morpho-first agentic lending workflow for Api3-backed markets, including feed readiness checks, guarded funding, oracle adapter deployment, market deployment, and verification when the request and environment support signer-backed execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daav3](https://clawhub.ai/user/daav3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan, dry-run, and, with explicit signer-backed approval, execute Morpho market workflows for selected collateral and borrow assets backed by Api3 feeds. It helps resolve oracle routes, classify or fund feeds, deploy the Morpho oracle adapter and market, and report verified outcomes or blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-authority on-chain financial actions, including feed funding and market deployment. <br>
Mitigation: Use planning, preflight, dry-run, and approval-summary review before any signer-backed execution, and require explicit user approval for transaction submission. <br>
Risk: Signer material can be exposed if raw private keys are placed in request files or chat. <br>
Mitigation: Use environment variables such as LIVE_SIGNER_ENV or an external signer, and keep generated request files and run directories private. <br>
Risk: A funding transaction or dry-run plan can be mistaken for a verified live Morpho market. <br>
Mitigation: Claim completion only after the run proves live feed readiness, adapter handoff, market creation, positive oracle verification, and rollback-plan inspection. <br>
Risk: Bundled feed and market snapshots may be stale for live deployment decisions. <br>
Mitigation: Prefer live RPC-backed checks for current on-chain claims and treat packaged data as fallback planning evidence. <br>
Risk: Lower-level EVK or Euler commands may invoke broader tooling outside the intended Morpho workflow. <br>
Mitigation: Prefer the agentic-lending-morpho wrapper for normal runs and use lower-level commands only for deliberate debugging or resume operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daav3/agentic-lending-morpho) <br>
- [Project homepage](https://github.com/daav3/agentic-lending-project) <br>
- [Workflow](references/workflow.md) <br>
- [Current capabilities and limits](references/current_capabilities.md) <br>
- [Morpho oracle adapter](references/morpho-oracle-adapter.md) <br>
- [Feed-to-market state machine](references/state-machine.md) <br>
- [Wrapper summary contract](references/summary-contract.md) <br>
- [Live request template](references/live-request-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON artifacts and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit or inspect request files, approval summaries, run directories, rollback plans, progress logs, deployment artifacts, and verification summaries.] <br>

## Skill Version(s): <br>
0.1.11 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
