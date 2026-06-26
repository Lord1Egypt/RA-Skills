## Description: <br>
Email Pro Optimized is a high-performance mail management skill for QQ, Gmail, and Outlook that can list accounts, read, search, fetch, analyze, and send email with IMAP/SMTP, OAuth 2.0, and concurrent processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q012315](https://clawhub.ai/user/q012315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to manage configured QQ, Gmail, and Outlook mailboxes, including checking recent or unread messages, searching and fetching message contents, sending messages with optional HTML or attachments, and automating email monitoring or backup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials and OAuth tokens. <br>
Mitigation: Protect ~/.openclaw/credentials, verify requested mail permissions, and review credential file access before use. <br>
Risk: The Outlook quick-authorization path includes bundled OAuth application credentials. <br>
Mitigation: Use your own Gmail or Outlook OAuth application credentials instead of bundled quick-auth values. <br>
Risk: Bundled developer scripts can push or synchronize local repository or workspace files if run. <br>
Mitigation: Avoid running auto-push.py or sync-updates.py unless repository or workspace changes are intentional. <br>
Risk: Sending commands can transmit messages or attachments to unintended recipients. <br>
Mitigation: Confirm recipients, subject, body, HTML mode, and attachment paths before sending email. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/q012315/email-pro-optimized) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime commands return JSON records and text status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and requests; reads and writes mailbox credential and OAuth token files under ~/.openclaw/credentials.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
