## Description: <br>
A skill that helps an agent send email through an existing SMTP configuration, with support for HTML-formatted bodies and local file attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scccmsd](https://clawhub.ai/user/scccmsd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to send SMTP email from an agent workflow using a configured SMTP account, including optional HTML content or local file attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored SMTP credentials to send email and local file attachments to arbitrary recipients. <br>
Mitigation: Use a dedicated low-privilege SMTP or app password, lock down the SMTP configuration file, and confirm the recipient, subject, body source, and attachment paths before each use. <br>
Risk: The documentation advertises retry, logging, and markdown conversion safeguards that the implementation may not provide. <br>
Mitigation: Do not rely on those safeguards unless the implementation is updated and re-reviewed; test email behavior before operational use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/scccmsd/custom-smtp-sender) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and email body text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can trigger SMTP email delivery and attach local files when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
