## Description:

Agentic Lending EVK plans and runs guarded EVK-first Api3-backed lending workflows, including oracle route resolution, feed readiness or funding, EVK market deployment preparation, and optional live borrow proof when explicitly allowed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daav3](https://clawhub.ai/user/daav3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DeFi operators use this skill to prepare, dry-run, and, with explicit approval, execute Api3-backed EVK lending market workflows and post-deploy borrow canaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can send on-chain funding, deployment, approval, swap, and borrow-canary transactions.

Mitigation: Run preflight and preview first, and use live signer-backed execution only after explicit user approval.

Risk: Signer material or wallet details can be exposed if placed in request files or persisted artifacts.

Mitigation: Use signerEnvName with LIVE_SIGNER_ENV, keep secrets in local environment variables or runtime config, and disable artifact persistence when secrets are present.

Risk: Unlimited approvals and zero-slippage swaps can expose wallet funds.

Mitigation: Use exact approval scope unless unlimited approval is explicitly accepted, require nonzero amountOutMinimum, verify the router, and revoke allowances after tests.

Risk: Bundled feed-status and market-registry snapshots can be stale.

Mitigation: Prefer live RPC results or fresh operator-managed registry and feed-status inputs when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daav3/skills/agentic-lending-evk)
- [Project homepage](https://github.com/daav3/agentic-lending-project)
- [Agentic Lending EVK workflow reference](references/api_reference.md)
- [Current capabilities and limits](references/current_capabilities.md)
- [EVK wrapper summary contract](references/summary-contract.md)
- [EVK live borrow checklist](references/live-borrow-checklist.md)
- [Example request](references/example-request.json)
- [Live request template](references/live-request-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to run Node.js CLIs and produce persisted JSON artifacts when artifact persistence is enabled.]

## Skill Version(s):

0.1.16 (source: evidence.release.version, package.json, CHANGELOG released 2026-06-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
