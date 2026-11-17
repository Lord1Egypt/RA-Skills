## Description:

Queries configured email accounts over IMAP for a requested time range and produces structured summaries of important messages, sent mail, communication statistics, follow-up items, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jams-hub](https://clawhub.ai/user/jams-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fetch mailbox data for a requested date range and turn it into concise Chinese email summaries, communication statistics, pending follow-ups, and attachment lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read configured mailboxes over IMAP and may access more email than intended.

Mitigation: Install it only when mailbox access is intended, narrow invocation conditions, and require explicit confirmation before mailbox access.

Risk: Mail authorization codes are stored in plaintext in accounts.json.

Mitigation: Store authorization codes outside the skill directory when possible, restrict access to accounts.json, keep it out of version control and backups, and prefer revocable app-specific credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jams-hub/skills/email-query-summary)
- [SETUP.md](SETUP.md)
- [Aliyun Enterprise Mail](https://work.aliyun.com/alimail/)
- [QQ Mail](https://mail.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Simplified Chinese Markdown summaries; helper script returns JSON for the agent to summarize]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should omit account secrets, raw JSON, script code, and execution details from user-facing responses.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact manifest reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
