## Description: <br>
Send email through SMTP providers such as 126, QQ, Sina, or Aliyun Mail using an SMTP authorization code or mailbox password. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanmwx](https://clawhub.ai/user/seanmwx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to configure SMTP settings, validate them with a dry run, and send simple test emails through supported or custom providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback SMTP configuration can connect to an unintended provider or use mismatched credentials when settings are incomplete. <br>
Mitigation: Run `scripts/send_email.py --dry-run` first and confirm the resolved provider, host, username, sender, recipient, subject, and body before sending. <br>
Risk: SMTP credentials and message contents may be disclosed to the configured mail provider or recipient. <br>
Mitigation: Prefer provider-issued SMTP or app passwords, avoid primary mailbox passwords where possible, and do not send sensitive content unless that disclosure is intended. <br>
Risk: Non-126 providers can be misconfigured if the minimal `.env` values are used without explicit connection settings. <br>
Mitigation: For non-126 or custom providers, explicitly set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USE_SSL`, and `SMTP_USERNAME`. <br>


## Reference(s): <br>
- [SMTP provider notes](references/providers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with dotenv configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute a Python SMTP script that sends email when not run in dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
