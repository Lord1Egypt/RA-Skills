## Description: <br>
Read and send email through IMAP and SMTP with cached inbox checks, mailbox search, message state changes, attachment handling, replies, forwards, and Markdown-friendly CLI output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rashed-mamoon](https://clawhub.ai/user/rashed-mamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let an agent inspect inboxes, search email, fetch message content, send or reply to email, and manage attachments through standard IMAP/SMTP accounts. It is suited for mailbox automation where the operator can provide a scoped email account or app password. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires mailbox-level IMAP/SMTP credentials and can read or send email from the configured account. <br>
Mitigation: Use an app password or limited-purpose mailbox, keep .env permissions restricted with chmod 600, and avoid sharing the configured workspace. <br>
Risk: Delete, mark, download, and test commands can permanently change mailbox state, send a test email, or write files locally. <br>
Mitigation: Review commands and UIDs before execution, test with a non-critical mailbox first, and avoid delegating destructive commands without operator confirmation. <br>
Risk: Cached inbox data and downloaded attachments may contain sensitive content. <br>
Mitigation: Treat .cache and attachment directories as private data, clear them when no longer needed, and choose a controlled download directory. <br>
Risk: TLS certificate verification can be disabled through environment configuration. <br>
Mitigation: Keep IMAP_REJECT_UNAUTHORIZED and SMTP_REJECT_UNAUTHORIZED enabled except for controlled local testing with known servers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rashed-mamoon/email-suite-imap-smtp) <br>
- [Gmail app passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables, plain-text command output, shell commands, and .env configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read from or write to local cache and attachment files; may send, mark, delete, or download email when invoked with the relevant commands.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata; artifact package.json is 1.2.0 and CHANGELOG top entry is 1.2.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
