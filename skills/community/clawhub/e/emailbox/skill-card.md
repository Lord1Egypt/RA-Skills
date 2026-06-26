## Description: <br>
Emailbox is an IMAP/SMTP email toolkit for 12+ providers that helps agents send, receive, search, forward, schedule, and format emails with templates, attachments, and document-data workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and automation agents use Emailbox to operate authenticated mailboxes through IMAP/SMTP, including sending messages, reading and searching inboxes, forwarding mail, scheduling messages, and packaging document-derived content into email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials and sensitive email content. <br>
Mitigation: Use session-only environment variables or a system secret manager, avoid plaintext credential files, and prefer a dedicated low-privilege email account. <br>
Risk: Email sending or forwarding can expose sensitive documents or messages to unintended recipients. <br>
Mitigation: Verify recipients, attachments, and generated content before sending sensitive messages. <br>
Risk: Downloaded attachments from untrusted mail can be unsafe. <br>
Mitigation: Do not download attachments from untrusted senders until filename handling is tightened, and scan attachments before opening them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tobewin/emailbox) <br>
- [Provider Configuration Guide](artifact/references/providers.md) <br>
- [Document Integration Workflows](artifact/references/integrations.md) <br>
- [HTML Email Templates](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash command examples, email text or HTML content, local queue files, and downloaded attachment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus EMAIL_ADDRESS and EMAIL_AUTH, or provider-specific EMAIL_* and EMAIL_*_AUTH environment variables.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
