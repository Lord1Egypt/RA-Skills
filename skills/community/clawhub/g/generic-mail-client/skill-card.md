## Description: <br>
Send, receive, and manage emails via IMAP/POP3 and SMTP for multiple accounts with support for text, HTML, attachments, folders, and read status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuwenke123](https://clawhub.ai/user/xuwenke123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with configured mailbox accounts: sending email, listing and reading messages, and updating IMAP message state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email and mutate mailbox state without visible confirmation or send-safety controls. <br>
Mitigation: Require host-side confirmation and limits around sending, Bcc, attachments, and mailbox moves before enabling it for routine use. <br>
Risk: Mailbox credentials give broad access if configured with a primary personal password. <br>
Mitigation: Install only with a dedicated mailbox or app-specific password and avoid personal primary passwords. <br>
Risk: Dependency provenance may be insufficient for sensitive environments. <br>
Mitigation: Regenerate dependencies from a trusted HTTPS registry before relying on the skill in a sensitive environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuwenke123/generic-mail-client) <br>
- [Publisher profile](https://clawhub.ai/user/xuwenke123) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Structured email operation results and mailbox metadata, with configuration supplied as YAML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send email or mutate mailbox state through the configured host environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
