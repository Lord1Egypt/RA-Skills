## Description: <br>
CLI to manage emails via IMAP/SMTP; use himalaya to list, read, write, reply, forward, search, and organize emails from the terminal, with support for multiple accounts and MML message composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and email power users use this skill to configure Himalaya and operate mailboxes from an agent-guided terminal workflow. It helps with listing, searching, reading, composing, replying, forwarding, moving, deleting, flagging, and downloading email content across configured accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands that access or change configured mailboxes. <br>
Mitigation: Install and use it only when comfortable granting Himalaya access to configured email accounts, and review mailbox, folder, and message identifiers before running commands. <br>
Risk: Email credentials may be exposed if raw passwords are stored in configuration files. <br>
Mitigation: Prefer pass, a system keyring, or another secret manager, and keep Himalaya configuration file permissions tight. <br>
Risk: Sending, deleting, moving, or downloading mail can affect real recipients and mailbox state. <br>
Mitigation: Confirm account, recipient, folder, message ID, and attachment paths before executing those operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/utromaya-code/email-cli-manager) <br>
- [Himalaya project homepage](https://github.com/pimalaya/himalaya) <br>
- [Himalaya Configuration Reference](references/configuration.md) <br>
- [Message Composition with MML](references/message-composition.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, TOML configuration examples, and email template snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe JSON or plain Himalaya command output and MML message templates; no structured API response is produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
