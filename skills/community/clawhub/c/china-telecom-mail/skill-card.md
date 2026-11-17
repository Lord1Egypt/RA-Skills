## Description:

Send and receive emails via China Telecom (POP3:995, SMTP:465). Lists today's emails, reads content, forwards emails, and sends new emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang-wh](https://clawhub.ai/user/williamwang-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mailbox users use this skill to automate China Telecom mailbox workflows, including listing today's messages, reading mail, generating JSON summaries, sending messages, and forwarding selected email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read mailbox contents from the configured China Telecom account.

Mitigation: Use only with a mailbox you control and review access before installation.

Risk: The skill can send or forward emails and attach arbitrary local files.

Mitigation: Require explicit user confirmation for each send, forward, and attachment action, and do not let untrusted email content choose recipients or file paths.

Risk: Mailbox credentials are stored in a plain config.toml file.

Mitigation: Prefer a revocable mail authorization code over a primary password and restrict config.toml file permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/williamwang-wh/skills/china-telecom-mail)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text and JSON responses from command-line mail actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and python. Reads credentials from config.toml and connects to China Telecom POP3 and SMTP servers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
