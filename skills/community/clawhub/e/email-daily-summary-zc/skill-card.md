## Description:

Automatically logs into email accounts (Gmail, Outlook, QQ Mail, etc.) and generates daily email summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Users who need recurring mailbox digests can use this skill to open supported webmail sessions, review recent messages, produce concise summaries and statistics, and prepare daily email reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires broad authenticated mailbox access and may expose sensitive message data through screenshots, logs, or generated summaries.

Mitigation: Use a dedicated browser profile or read-only mailbox account, avoid capturing unnecessary mailbox content, and treat all generated artifacts as sensitive.

Risk: Manual login examples can encourage users to enter real credentials into shell-driven workflows.

Mitigation: Prefer an existing browser session and avoid putting passwords or tokens in commands, scripts, or logs.

Risk: Cron or launchd automation can run mailbox collection unattended.

Mitigation: Enable schedules only after reviewing the command path, output locations, and disable procedure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/email-daily-summary-zc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce email summary reports, mailbox statistics, screenshots, logs, and scheduled-task configuration examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
