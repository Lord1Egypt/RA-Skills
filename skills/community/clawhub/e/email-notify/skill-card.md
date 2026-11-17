## Description:

Send SMTP email notifications after Codex completes a task. Use when one Codex or Claude run is finished, or when you need to notify on task completion with device name, project name, status, and summary via email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caopulan](https://clawhub.ai/user/caopulan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send task-completion notifications by SMTP after Codex or Claude runs, including the device name, project name, status, and summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task titles, project names, machine names, statuses, and summaries may be sent to configured email recipients and the SMTP provider.

Mitigation: Avoid secrets and sensitive client details in summaries, and use manual invocation instead of auto-notification instructions when per-run control is needed.

Risk: SMTP credentials are configured through environment variables for the notification script.

Mitigation: Use an app-specific SMTP password where possible and configure TLS or SSL consistently for the selected SMTP service.

## Reference(s):

- [Email Notify ClawHub Skill Page](https://clawhub.ai/caopulan/skills/email-notify)
- [Publisher Profile](https://clawhub.ai/user/caopulan)
- [send_email_notification.py](artifact/scripts/send_email_notification.py)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send an SMTP email containing task title, project name, machine name, status, and summary when the helper script is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
