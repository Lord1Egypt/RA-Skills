## Description:

Smart Asistant Mail is an OpenClaw Gmail agent skill for reading inboxes, searching messages, organizing labels, classifying priority and spam, drafting replies, scheduling checks, reporting activity, and tracking email automation costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coorops25](https://clawhub.ai/user/coorops25)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators use this skill to manage Gmail workflows through an agent, including inbox review, label routing, spam triage, reply drafting, scheduled monitoring, and daily or weekly email summaries. It is intended for accounts where delegated Gmail access and supervised mailbox automation are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests durable Gmail mailbox access and can read, search, label, archive, trash, draft, and send email through connected tools.

Mitigation: Install only for accounts where delegated Gmail automation is acceptable, use the minimum viable account scope, and review all requested mailbox actions before enabling automation.

Risk: Scheduled checks and automatic routing can change mailbox state without enough user control if cron jobs, heartbeat behavior, or notification targets are unclear.

Mitigation: Keep automatic mode disabled until schedules, quiet hours, notification channels, deactivation steps, and review or quarantine behavior are confirmed.

Risk: Persistent learned rules may archive, route, or suppress future email incorrectly.

Mitigation: Require explicit approval for persistent rule changes and periodically audit learned rules, spam handling, and email action logs.

Risk: Setup and diagnostics reference API keys and account identifiers that could be exposed in terminal output or logs.

Mitigation: Avoid commands or setup paths that print secrets, keep environment variables out of shared logs, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/coorops25/skills/emailagy)
- [Cost optimization reference](artifact/references/cost-optimization.md)
- [Learning patterns reference](artifact/references/learning-patterns.md)
- [Email heartbeat template](artifact/assets/HEARTBEAT.email.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Gmail query examples, JSON configuration snippets, and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Gmail searches, label changes, draft replies, cron schedules, budget summaries, and rule updates for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
