## Description:

Secure, safe-by-default Fastmail integration for email, contacts, and calendar via JMAP and CalDAV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tassiedaddy](https://clawhub.ai/user/tassiedaddy)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to verify Fastmail setup, triage and search email, inspect threads, read contacts, view upcoming calendar events, and optionally perform explicitly enabled email and calendar writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fastmail credentials and account data may be sent to configurable or discovered network destinations.

Mitigation: Use the default Fastmail endpoints, avoid custom FASTMAIL_BASE_URL and FASTMAIL_CALDAV_BASE_URL values, and review destination settings before use.

Risk: Email, contact, and calendar output can expose private account content despite default redaction.

Mitigation: Keep FASTMAIL_REDACT enabled, avoid --raw unless necessary, and use narrow read-only tokens for normal workflows.

Risk: Write-enabled operation can send email or create, update, or delete calendar data.

Mitigation: Leave FASTMAIL_ENABLE_WRITES unset for routine use and provide write-capable credentials only for deliberate send or calendar modification tasks.

## Reference(s):

- [Fastmail Suite on ClawHub](https://clawhub.ai/tassiedaddy/skills/fastmail-suite)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain private account data; redaction is enabled by default unless raw output is requested.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
