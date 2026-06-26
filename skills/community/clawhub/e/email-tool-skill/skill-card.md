## Description: <br>
Send mail with Python stdlib smtplib (SMTP_SSL to smtp.yeah.net:465). Documented account validates@yeah.net with embedded client auth code; standalone script e.g. /tmp/send_email.py, no TTY, no skill-local bash tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WGY2e](https://clawhub.ai/user/WGY2e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create and run a one-shot Python script that sends plain-text email through SMTP_SSL without local mail tools or interactive prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a live shared SMTP credential that could be used to send mail as the documented account. <br>
Mitigation: Install only when authorized to use the account, replace the credential with a securely managed secret, and rotate the exposed authorization code. <br>
Risk: The generated script can send arbitrary email without built-in per-send confirmation. <br>
Mitigation: Review the sender, recipient, subject, and body before execution, and restrict use to approved recipients and content. <br>


## Reference(s): <br>
- [Python smtplib documentation](https://docs.python.org/3/library/smtplib.html) <br>
- [ClawHub skill page](https://clawhub.ai/WGY2e/email-tool-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a standalone Python email-sending script and run command; requires python3 and SMTP credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
