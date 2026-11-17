## Description:

Defensive triage for OpenClaw, Hermes Agent, local host telemetry, and skill-supply-chain scanning that separates verified evidence from suspicion and keeps remediation explicitly authorized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-allen-oneal](https://clawhub.ai/user/jason-allen-oneal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to triage OpenClaw, Hermes Agent, local host, and skill supply-chain evidence before making authorized remediation decisions. It helps separate verified facts, suspicions, unknowns, next steps, and actions that should wait for explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence OpenClaw skill installation and quarantine workflows.

Mitigation: Install it only when that administrative influence is intended, and keep installation, replacement, and quarantine actions explicitly authorized by the operator.

Risk: Quarantine can temporarily disable an active skill, and one quarantine path relies on operator discipline rather than an enforced evidence check.

Mitigation: Run quarantine only after independently verified high-risk evidence, preserve the scan report, and confirm the target is an installed skill inside the active managed skill tree.

Risk: Operator-controlled command and endpoint variables can redirect scanner, ClawHub, OpenClaw, or browser health behavior.

Mitigation: Keep SENTINAL_SCANNER_CMD, SENTINAL_CLAWHUB_CMD, OPENCLAW_BIN, and endpoint variables under operator control, and prefer pinned or vetted CLI tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-allen-oneal/skills/active-defense-sentinal)
- [OpenClaw compatibility review](COMPATIBILITY.md)
- [Allowed and Blocked Actions](references/allowed-blocked-actions.md)
- [Evidence Template](references/evidence-template.md)
- [Hermes Adapter](references/hermes-adapter.md)
- [Host Guard Adapter](references/host-guard-adapter.md)
- [OpenClaw Adapter](references/openclaw-adapter.md)
- [Quarantine Policy](references/quarantine-policy.md)
- [Risk Matrix](references/risk-matrix.md)
- [Scan Workflow](references/scan-workflow.md)
- [Skill Scanner Adapter](references/skill-scanner-adapter.md)
- [OpenClaw upstream compatibility baseline](https://github.com/openclaw/openclaw/tree/31157a19b41dae0ec28a4010d08656d11f55c067)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise triage summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates verified facts, suspected issues, unknowns, recommended next steps, and actions deferred pending authorization.]

## Skill Version(s):

0.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
