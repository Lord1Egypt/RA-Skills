## Description:

Email Reader helps an agent read, summarize, classify, and send email through the himalaya IMAP/SMTP CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackeven02](https://clawhub.ai/user/jackeven02)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to give an agent mailbox workflows such as reading recent messages, summarizing unread mail, searching messages, flagging important items, and drafting or sending email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive mailbox contents and may grant the agent authority to send or modify messages.

Mitigation: Use a least-privilege account, require user confirmation before sending or deleting email, and review mailbox access before deployment.

Risk: Credential examples include passwords or app passwords in CLI configuration, which can be leaked through shell history, logs, or configuration files.

Mitigation: Prefer provider-supported OAuth, keychain, or secret-helper flows, and avoid entering real passwords directly in shell commands.

Risk: The workflow depends on installing and trusting the himalaya CLI.

Mitigation: Pin or verify the CLI package and installation source before use.

## Reference(s):

- [Email management reference resources](references/resources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with email summaries, suggested actions, and inline himalaya shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sender, subject, summary, received-time context, and recommended actions such as reply, delete, or mark.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
