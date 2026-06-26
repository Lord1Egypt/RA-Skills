## Description: <br>
Multi-account email management skill for IMAP/SMTP that fetches, reads, searches, composes, sends, replies, forwards, and organizes emails across multiple accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[borgcube](https://clawhub.ai/user/borgcube) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to automate mailbox workflows across configured IMAP/SMTP accounts, including fetching, reading, searching, composing, sending, replying, forwarding, archiving, and rule-based processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, send, modify, and automate actions across configured mailboxes. <br>
Mitigation: Grant access only to accounts and folders intended for automation, and review configuration before enabling live send, move, archive, or heartbeat workflows. <br>
Risk: Forwarding, auto-reply, mail-merge, fallback SMTP, and webhook rules can disclose email content or send unintended messages. <br>
Mitigation: Review each rule and recipient target, avoid catch-all rules, test with dry-run or limited accounts where available, and approve external webhook destinations before use. <br>
Risk: Plaintext credentials or command-line password flags can expose mailbox secrets. <br>
Mitigation: Use 1Password, macOS Keychain, or environment-backed credential references, keep TLS enabled, and avoid storing secrets directly in configuration files. <br>
Risk: Heartbeat state, queues, drafts, attachments, and mailbox processing files may contain sensitive email metadata or message content. <br>
Mitigation: Store generated state and output files only in private locations with appropriate filesystem permissions and retention controls. <br>


## Reference(s): <br>
- [clawMail Skill - API Reference](references/REFERENCE.md) <br>
- [Processing Rules Reference](references/RULES.md) <br>
- [Email Templates Reference](references/TEMPLATES.md) <br>
- [ClawHub skill page](https://clawhub.ai/borgcube/claw-mail) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/borgcube) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples, JSON script outputs, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may read or write email messages, attachments, mailbox state, drafts, queues, and configuration-driven rule actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
