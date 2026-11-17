## Description:

Create disposable Mail.tm inboxes and programmatically read incoming emails/OTP codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantaclaw-ai](https://clawhub.ai/user/fantaclaw-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test automation engineers use this skill to create disposable test inboxes, poll incoming email, and extract OTP codes while validating email verification flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tokens, passwords, saved JSON, message bodies, and OTPs may expose mailbox access or verification secrets.

Mitigation: Treat these values as sensitive, avoid logging or sharing them unnecessarily, keep tokens private, and delete saved result files when finished.

Risk: Disposable inboxes may be blocked by some production services or fail reliability expectations in CI.

Mitigation: Use the skill for disposable testing inboxes only and prefer stable paid inbox providers when reliability is critical.

## Reference(s):

- [Disposable Email on ClawHub](https://clawhub.ai/fantaclaw-ai/skills/disposable-email)
- [Mail.tm API endpoint](https://api.mail.tm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script output can include disposable inbox addresses, passwords, bearer tokens, message bodies, and OTP values.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
