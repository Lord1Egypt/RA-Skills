## Description:

Run a non-interactive OpenClaw security audit that produces a structured BLUF report with posture rating, ranked findings, and one-line fix commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infectit007](https://clawhub.ai/user/infectit007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to run OpenClaw security audits and convert the audit output into a concise BLUF report for scheduled checks, configuration changes, or briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact's safety claims conflict with delivery paths that can persist reports or send audit contents externally.

Mitigation: Use stdout-only unless persistent records or Telegram delivery are explicitly required, and confirm destination, retention, and redaction before use.

Risk: Telegram delivery can read environment credentials and transmit security report content outside the local machine.

Mitigation: Enable Telegram only after approving external delivery and verifying the intended bot token, chat ID, and data handling process.

Risk: The cron example can create recurring audits that repeatedly route security report data.

Mitigation: Confirm the schedule, destination, retention, redaction, and removal process before enabling the scheduled job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infectit007/skills/eva-security-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown BLUF report with severity sections, posture rating, next steps, and command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-interactive; can produce stdout output and may describe optional memory, Telegram, or scheduled delivery paths.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
