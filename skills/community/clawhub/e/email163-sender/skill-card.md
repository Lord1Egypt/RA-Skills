## Description: <br>
Email163 Sender sends email through a 163 mailbox using an authorization code, with support for plain text, HTML, attachments, CC, and BCC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imnull](https://clawhub.ai/user/imnull) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send email from a configured 163 mailbox, including text or HTML messages, attachments, and optional CC or BCC recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 163 authorization code and can send email from the configured mailbox. <br>
Mitigation: Review recipients, subject, body, CC/BCC, and attachments before each send, and prefer environment variables over command-line arguments for the authorization code. <br>
Risk: The security summary states that TLS certificate verification is disabled. <br>
Mitigation: Prefer a version that keeps normal TLS certificate verification enabled before using the skill for sensitive or production email. <br>
Risk: The security summary states that sensitive sent-mail metadata is stored locally. <br>
Mitigation: Protect the .email_history directory and clear history when retention is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imnull/email163-sender) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [CLI text output with local JSON history records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends mail through 163 SMTP and can create or update .email_history/sent_emails.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
