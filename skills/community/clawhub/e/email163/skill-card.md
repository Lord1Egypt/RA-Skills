## Description:

This skill provides a Go-based 163 Mail SMTP sender that supports HTML email, multiple recipients, command-line usage, and daily send logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x760591483](https://clawhub.ai/user/x760591483)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to understand, build, and run a command-line mail sender for 163 Mail SMTP. It is suited for sending HTML notifications to one or more recipients when the required 163 Mail address and authorization code are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP certificate checks are disabled.

Mitigation: Remove InsecureSkipVerify and require normal TLS certificate verification before using real mail credentials.

Risk: Email details are logged by default, including subject, recipients, content excerpts, and send result.

Mitigation: Make logs opt-in, keep log directories private, and redact sensitive message content before production use.

Risk: Real mail credentials are required through environment variables.

Mitigation: Use a 163 Mail authorization code stored in a secret manager or protected runtime environment, and do not commit credentials.

Risk: Untrusted subject text may be unsafe until header validation is added.

Mitigation: Do not pass untrusted text as the subject unless header validation is implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x760591483/skills/email163)
- [Publisher profile](https://clawhub.ai/user/x760591483)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Go source code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI uses EMAIL163_ADDRESS and EMAIL163_PASSWORD environment variables, accepts subject, content, recipients, and log path flags, and can write daily log files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
