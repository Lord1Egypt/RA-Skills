## Description:

邮件日报专业版 helps enterprise managers, team leads, and operations users aggregate multiple mailboxes, generate AI-assisted email digests, schedule reports, classify messages, trigger alerts, and analyze email trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, team leads, and operations staff use this skill to consolidate mailbox activity, produce daily or scheduled email reports, classify important messages, and route notifications to trusted channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles mailbox contents and may send email-derived summaries to third-party channels.

Mitigation: Use only trusted mailboxes and push destinations, and confirm exactly what email content is included before enabling push, alert, or scheduled report workflows.

Risk: SMTP passwords and webhook secrets may be stored or passed through configuration.

Mitigation: Keep credentials out of committed config files, prefer protected secret storage or environment variables, and rotate any exposed webhook or SMTP credentials.

Risk: Scheduled monitoring and real-time alerts can repeatedly process mailbox data without active user review.

Mitigation: Disable scheduled monitoring unless it is needed, scope monitored accounts and alert rules narrowly, and review execution history regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-digest-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command examples, JSON configuration snippets, and text, HTML, Markdown, JSON, or CSV report outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mailbox summaries, message priority scores, action suggestions, logs, scheduled report state, alert history, and external notification payloads.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
