## Description:

163邮箱助手专业版 helps agents manage 163 mailboxes for bulk sending, advanced search, scheduled tasks, archiving, audit logs, templates, and multi-account workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operations teams, and enterprise mailbox administrators use this skill to guide bulk 163 email handling, mailbox search and export, scheduled cleanup, archiving, audit review, template-based sending, and multi-account setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk sending, deletion, movement, archiving, and scheduled mailbox actions can affect many messages or recipients at once.

Mitigation: Use preview or dry-run for bulk actions, require confirmation before sending or deleting at scale, and keep recovery procedures and logs available.

Risk: The skill requires access to configured 163 mailboxes and may handle sensitive email content, recipient lists, and authorization codes.

Mitigation: Use only mailboxes the operator controls, protect authorization codes with environment variables or approved secret storage, and avoid exposing secrets in prompts, logs, or generated files.

Risk: Scheduled deletion or cleanup can run without immediate human review after configuration.

Mitigation: Enable scheduled deletion only after scopes, retention rules, audit logging, and notification behavior are reviewed and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-163-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSON, CSV, HTML, and text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe dry-run previews, exported search results, audit logs, mailbox configuration, scheduled actions, and command outcomes.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
