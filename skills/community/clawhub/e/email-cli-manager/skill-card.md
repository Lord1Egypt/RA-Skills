## Description:

CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language).

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate the Himalaya email CLI for listing, reading, searching, composing, replying, forwarding, moving, deleting, and organizing email from a terminal. It also guides configuration for multiple accounts, secure credential handling, attachments, and structured command output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps operate an email account, including send, delete, move, attachment download, and message selection actions.

Mitigation: Review recipients, message IDs, folder names, attachment paths, and delete or send commands before running them.

Risk: Email account configuration can expose credentials if plaintext passwords are stored in config files.

Mitigation: Prefer keyring, password-manager, or command-based credential storage over plaintext config values.

## Reference(s):

- [Himalaya project homepage](https://github.com/pimalaya/himalaya)
- [Himalaya Configuration Reference](references/configuration.md)
- [Message Composition with MML](references/message-composition.md)
- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/email-cli-manager)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples for email account operations and configuration.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
