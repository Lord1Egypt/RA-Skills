## Description:

163邮箱助手免费版 helps agents send, read, search, organize, and download attachments from a 163 mailbox using command-line workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate routine 163 mailbox tasks such as sending messages with attachments, reading or searching messages, managing folders, and downloading attachments. It is intended for personal and lightweight workflow use where the agent can access a configured mailbox authorization code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox authorization codes can expose sensitive email access if stored or shared carelessly.

Mitigation: Use a dedicated or low-risk mailbox where possible, store the client authorization code securely, and avoid placing credentials in version-controlled files.

Risk: Delete and move commands can alter mailbox state if the wrong message ID is used.

Mitigation: Search or read messages first, confirm the exact message ID and target folder, and require explicit confirmation before destructive operations.

Risk: Downloaded attachments may contain untrusted content.

Mitigation: Download attachments only to a controlled folder after verifying the sender, message context, and file name.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/email-163-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include mailbox operation status, message summaries, search results, attachment handling guidance, and setup instructions.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
