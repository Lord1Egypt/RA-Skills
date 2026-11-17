## Description:

Helps operators diagnose and repair OpenClaw host, gateway, plugin, cron, model, channel, approval, and update problems through focused checks and verified fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkf-gitty](https://clawhub.ai/user/bkf-gitty)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and developers use this skill to investigate live host failures, plan scoped repairs, and verify gateway, plugin, job, model, channel, or update health after changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host repairs could change configuration, plugins, scheduled jobs, service state, or model routes.

Mitigation: Review and approve proposed production changes, back up state, make the smallest targeted repair, and verify the affected services afterward.

Risk: Troubleshooting may expose credentials or sensitive host data.

Mitigation: Prefer redacted diagnostics and metadata; inspect raw secrets or workspace contents only with explicit approval.

Risk: Restarting or updating a gateway may interrupt an agent running inside it.

Mitigation: Arrange a continuation path before service changes and verify host health after restart.

## Reference(s):

- [Claw Mechanic release](https://clawhub.ai/bkf-gitty/skills/claw-mechanic)
- [Root Failure Taxonomy](artifact/references/root-failure-taxonomy.md)
- [Claw Mechanic Failure Map](artifact/references/failure-map.md)
- [Host Profile Template](artifact/references/host-profile-template.md)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Diagnostic guidance, Repair plans, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports findings, verification evidence, unresolved issues, and recommended next actions.]

## Skill Version(s):

1.1.0 (source: ClawHub server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
