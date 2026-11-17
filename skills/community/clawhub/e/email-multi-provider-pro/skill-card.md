## Description:

多邮箱管理专业版 helps agents manage Gmail, Outlook, and Exchange mailboxes across multiple profiles with bulk operations, filtering, templates, exports, and audit-oriented workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, enterprise teams, support teams, operations teams, and developers can use this skill to coordinate multi-account mailbox workflows, automate bulk email handling, export filtered results, and maintain audit-oriented operational records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk mailbox actions can send, reply, forward, delete, archive, tag, or export many messages at once.

Mitigation: Require dry-run previews and human approval before bulk execution, use rate limits, and apply least-privilege mailbox scopes.

Risk: The skill depends on mailbox credentials, profile switching, callback URLs, and optional API-key authentication.

Mitigation: Use only intended mailbox accounts, restrict callback URLs, store credentials in a keychain or managed secret store, and verify how porteden stores tokens before use.

Risk: Exports and audit logs can contain sensitive email content, recipients, subjects, and operational history.

Mitigation: Limit export destinations, encrypt or access-control logs, configure retention, and review shared reports before distribution.

Risk: The skill produces shell commands for an external mailbox CLI, so generated commands may have real account impact.

Mitigation: Review commands before execution, allow only expected porteden email/profile/audit commands, and avoid interpolating untrusted input into shell arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-multi-provider-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON/CSV configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose mailbox CLI operations, bulk-processing settings, templates, exports, and audit log workflows.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
