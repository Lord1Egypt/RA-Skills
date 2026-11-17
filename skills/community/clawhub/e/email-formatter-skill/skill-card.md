## Description:

Transform rough email drafts into polished, professional messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cerbug45](https://clawhub.ai/user/cerbug45)

### License/Terms of Use:

MIT

## Use Case:

Employees and external users use this skill to improve email grammar, clarity, tone, and business formatting while preserving the sender's intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may modify the host environment.

Mitigation: Review setup steps before installation, use an isolated virtual environment, and avoid --break-system-packages.

Risk: Confidential email drafts may be exposed if temporary-file handling is unsafe.

Mitigation: Do not process confidential drafts unless temporary-file handling is fixed or disabled; redact sensitive content when possible.

Risk: Broad security-scanning behavior may be under-scoped for an email formatter.

Mitigation: Review scanner behavior before deployment and keep security checks focused on email-formatting risks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cerbug45/skills/email-formatter-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with formatted email text and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include refusal or warning guidance for high-risk email content]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
