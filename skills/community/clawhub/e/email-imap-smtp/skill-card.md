## Description: <br>
Connect to mainstream email providers and perform reliable send/receive workflows through IMAP and SMTP with password or OAuth2 authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WaziXuan](https://clawhub.ai/user/WaziXuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect user-selected mailboxes, check IMAP/SMTP access, list or read messages, refresh OAuth2 tokens, and send email with optional HTML or attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox credentials or OAuth tokens can grant access to sensitive email. <br>
Mitigation: Use app passwords or scoped OAuth tokens where possible, keep credentials out of chat and logs, and install only when the skill is trusted with the selected mailbox. <br>
Risk: Email or attachments could be sent to unintended recipients or expose sensitive content. <br>
Mitigation: Require a final review of recipients, subject, body, and attachments before sending. <br>
Risk: Custom IMAP, SMTP, or OAuth endpoints could expose credentials or tokens if they are incorrect or untrusted. <br>
Mitigation: Verify custom IMAP/SMTP/OAuth endpoints before use. <br>


## Reference(s): <br>
- [Provider presets](references/provider-presets.md) <br>
- [ClawHub skill page](https://clawhub.ai/WaziXuan/email-imap-smtp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-like command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Email operations depend on user-supplied credentials, provider endpoints, mailbox filters, message UIDs, recipients, body content, and attachment paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
