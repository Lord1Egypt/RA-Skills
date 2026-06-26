## Description: <br>
Complete email management for Postfix/Dovecot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soderholmm](https://clawhub.ai/user/soderholmm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let OpenClaw agents manage a Postfix/Dovecot mailbox, including reading, searching, drafting, sending, moving, deleting, and managing spam folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad non-interactive access to a private mailbox, including sending messages and permanently deleting mail. <br>
Mitigation: Use a dedicated mailbox or app-specific password and require manual confirmation before sending, moving, deleting, emptying trash or spam, or acting on email content. <br>
Risk: Mailbox credentials may be stored in config.json or environment variables. <br>
Mitigation: Keep config.json out of version control, restrict file permissions, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soderholmm/email-manager) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, JSON configuration, and optional JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses non-interactive Python standard-library IMAP and SMTP helpers.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
