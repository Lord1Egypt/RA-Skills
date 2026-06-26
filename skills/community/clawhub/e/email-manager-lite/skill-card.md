## Description: <br>
Lightweight email manager with IMAP/SMTP support, advanced search, folder management, and attachment detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jorgermp](https://clawhub.ai/user/jorgermp) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users and developers use this skill to send, read, search, and organize email through IMAP and SMTP providers such as Zoho Mail, Gmail, Outlook, iCloud Mail, or custom mail servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials and mailbox contents. <br>
Mitigation: Install only when mailbox access is acceptable, use an app password or dedicated mailbox, and avoid sharing command output that contains sensitive email content. <br>
Risk: The artifact disables IMAP certificate validation. <br>
Mitigation: Remove the rejectUnauthorized: false IMAP setting before use so TLS certificates are validated. <br>
Risk: Send and move commands can change mailbox state. <br>
Mitigation: Require manual review before any send or move command, especially when operating on UIDs returned by search or read commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jorgermp/email-manager-lite) <br>
- [Zoho Mail App Passwords](https://accounts.zoho.eu/home#security/apppasswords) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue email send, read, search, folder listing, and move operations when configured with mailbox credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
