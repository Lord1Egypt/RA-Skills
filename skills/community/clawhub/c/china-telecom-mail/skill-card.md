## Description: <br>
Send and receive emails via China Telecom (POP3:995, SMTP:465), including listing today's emails, reading content, forwarding emails, and sending new emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwang-wh](https://clawhub.ai/user/williamwang-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to automate China Telecom mailbox workflows: checking today's messages, reading full email content, exporting summaries as JSON, sending email, and forwarding received messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive mailbox credentials to read from POP3 and send through SMTP. <br>
Mitigation: Use a dedicated or app-specific mailbox credential, restrict permissions on config.toml, and keep the file out of version control. <br>
Risk: The skill can send or forward messages and attachments from command-line inputs. <br>
Mitigation: Require explicit user confirmation before sending, forwarding, or attaching files, and verify recipients, subject, body, and attachment path before execution. <br>
Risk: Email reads and JSON summaries may expose personal, confidential, or regulated message content. <br>
Mitigation: Limit use to authorized mailboxes and redact or minimize email content before sharing summaries with downstream tools or logs. <br>


## Reference(s): <br>
- [China Telecom Mail Skill Page](https://clawhub.ai/williamwang-wh/china-telecom-mail) <br>
- [Publisher Profile: williamwang-wh](https://clawhub.ai/user/williamwang-wh) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output and JSON email summaries; email send and forward actions run from command-line arguments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, uv, OpenClaw, and configured China Telecom POP3/SMTP mailbox credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
