## Description:

Use when updating OpenClaw or debugging an OpenClaw instance after an update. This skill acts as a structured update runbook with emphasis on gateway startup, service-manager state, plugin registry and install drift, bundled-vs-npm/clawhub plugin confusion, stale config carried across upgrades, channel health, task ledger corruption, and logs that explain why the updated system is slow, disconnected, or half-broken.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkf-gitty](https://clawhub.ai/user/bkf-gitty)

### License/Terms of Use:

MIT

## Use Case:

Operators and engineers use this skill to plan OpenClaw updates, diagnose post-update regressions, verify service and plugin state, and choose the smallest repair that returns a host to a healthy state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting guidance can expose live channel tokens in terminal output, logs, or agent transcripts.

Mitigation: Do not run token-inspection commands that print raw values. If a token appears in a transcript, support ticket, log, or backup, rotate it and remove plaintext fallbacks after recovery.

Risk: Update, restart, or configuration-edit steps can affect a live OpenClaw host.

Mitigation: Use the skill only for explicit OpenClaw maintenance tasks, require confirmation before updates, restarts, or config edits, and verify host state before and after changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bkf-gitty/skills/claw-update-runbook)
- [Failure Patterns](references/failure-patterns.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic sequences, verification criteria, and handoff-note guidance; does not execute commands itself.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
