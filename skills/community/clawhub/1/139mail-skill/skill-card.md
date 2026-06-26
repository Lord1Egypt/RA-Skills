## Description: <br>
139mail sends and reads email through IMAP and SMTP for 139, QQ, 163, Gmail, and other mailbox providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chang-Tong](https://clawhub.ai/user/Chang-Tong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent send email, list mailbox messages, read message contents, and test mailbox connectivity after local IMAP/SMTP configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials and private email content. <br>
Mitigation: Use an app-specific password, restrict local configuration file permissions, and avoid connecting accounts that contain sensitive data unless the risk is acceptable. <br>
Risk: IMAP certificate verification is disabled in the artifact behavior. <br>
Mitigation: Avoid sensitive accounts until certificate verification is fixed and confirm mail server settings before use. <br>
Risk: Outgoing email and attachment actions may proceed without strong confirmation. <br>
Mitigation: Verify every recipient, message body, and attachment path before allowing the agent to send mail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Chang-Tong/139mail-skill) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Package manifest](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with CLI examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read private mailbox content and may send email or attachments through the configured account.] <br>

## Skill Version(s): <br>
1.0.0 (source: openclaw.skill.json, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
