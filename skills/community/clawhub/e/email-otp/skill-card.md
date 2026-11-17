## Description:

Create temporary email addresses and monitor for registration OTP codes or validation links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etopro](https://clawhub.ai/user/etopro)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to create disposable email inboxes, monitor incoming messages, and extract OTP codes or validation links during registration and verification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OTP codes, verification links, mailbox passwords, and JWT tokens may remain in plaintext files and terminal output.

Mitigation: Use the skill only for low-stakes disposable email workflows, avoid personal or account-recovery data, and delete ~/.tempmail_otp/ after use.

Risk: Persistent mailbox state can outlive the immediate verification task.

Mitigation: Review the generated files before installation or reuse, and clear stored state when the workflow is complete.

## Reference(s):

- [mail.tm API](https://api.mail.tm)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON CLI output, plus files containing the latest OTP code, validation link, and mailbox account state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent state under ~/.tempmail_otp/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
