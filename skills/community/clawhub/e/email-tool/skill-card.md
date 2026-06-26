## Description: <br>
Send and search emails via Zoho-compatible IMAP and SMTP using configured mailbox credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chowardcode](https://clawhub.ai/user/chowardcode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to send outbound email and search inbox messages through a configured Zoho or compatible IMAP/SMTP mailbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad ability to send email and read inbox contents. <br>
Mitigation: Use a dedicated or least-privileged mailbox, restrict who can invoke the skill, and require manual confirmation before sending messages or marking messages read. <br>
Risk: The security summary reports a vulnerable mail dependency. <br>
Mitigation: Upgrade nodemailer to a fixed major version before production use. <br>
Risk: Mailbox credentials are required for operation. <br>
Mitigation: Store credentials only in the external secrets file or environment variables and prefer app-specific credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chowardcode/email-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status messages and email search summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses external secrets from OPENCLAW_SECRETS_DIR/email-tool.json or environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
