## Description:

Send email through SMTP providers such as 126, QQ, Sina, or Aliyun Mail using an SMTP authorization code or mailbox password.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanmwx](https://clawhub.ai/user/seanmwx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex users use this skill to configure SMTP provider settings, validate email configuration with a dry run, and send simple test emails through supported mailbox providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP credentials could be placed in the public skill file's embedded configuration block.

Mitigation: Keep real credentials out of `SKILL.md`; use an untracked local env file or a proper secret store.

Risk: A real email send could expose content to the wrong recipient or fail because the provider expects an app-specific SMTP authorization code.

Mitigation: Run dry-run validation first, confirm sender and recipient values, and use provider-issued app-specific SMTP authorization codes where available.

## Reference(s):

- [SMTP Providers](references/providers.md)
- [ClawHub skill page](https://clawhub.ai/seanmwx/skills/email-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run validation steps and a real SMTP send command after sender, recipient, subject, body, and secret handling are confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
