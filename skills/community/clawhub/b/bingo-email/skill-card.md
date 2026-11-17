## Description:

Bingo Email lets an agent manage IMAP/SMTP mailboxes by reading, sending, replying to, forwarding, drafting, deleting, moving, and listing email through a Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soulcoolzzz](https://clawhub.ai/user/soulcoolzzz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent perform mailbox operations across providers such as QQ, 126/163, Gmail, Outlook, and custom IMAP/SMTP servers. It is suited to email triage, message drafting, replies, forwarding, folder management, and scripted mailbox workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access mailbox contents and send, forward, reply to, move, or delete email.

Mitigation: Review recipients, message bodies, reply-all actions, forwards, moves, and deletes before allowing an agent to execute them.

Risk: The local configuration stores an app password or authorization code for IMAP/SMTP access.

Mitigation: Keep ~/.config/bingo-email/config.toml private, preserve restrictive file permissions, and rotate the credential if it is exposed.

Risk: Weak transport or install choices can increase exposure when connecting to mail servers or installing the tool.

Mitigation: Use TLS or STARTTLS, do not use encryption = none, and prefer the reviewed packaged script over standalone curl installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soulcoolzzz/skills/bingo-email)
- [Project homepage](https://github.com/soulcoolzzz/bingo-email)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or modify mailbox state through IMAP/SMTP using local configuration at ~/.config/bingo-email/config.toml.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
