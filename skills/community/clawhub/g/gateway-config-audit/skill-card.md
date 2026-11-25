## Description:

Audit and harden a local OpenClaw configuration: inventory (doctor, status, config validate, security audit, secrets audit, automations list), triage by severity x interaction impact, then apply batch fixes with readback. Produces an evidence-backed issue list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw operators use this skill to audit local gateway configuration and state, prioritize findings by severity and interaction impact, and apply approved changes with backups and readback verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports instructions that bypass a database access guard.

Mitigation: Review the database-access instructions and remove or correct any guard-bypass steps before use.

Risk: The audit instructions require an external test message during a local audit.

Mitigation: Make live messaging optional and send a test message only with explicit owner approval.

Risk: ClawScan reports an unsafe maintenance sequence, and scan coverage was partial.

Mitigation: Review the maintenance sequence before use; require a verified backup and dry run before changes, and treat unreviewed behavior as unverified.

## Reference(s):

- [Session database growth triage](artifact/references/会话库膨胀分诊.md)
- [ClawHub skill page](https://clawhub.ai/zuoyunlai/skills/gateway-config-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown issue list with evidence, command examples, configuration guidance, and readback results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritized findings with severity, interaction impact, before-and-after values, backup paths, unresolved items, and owner-handled restart steps]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
