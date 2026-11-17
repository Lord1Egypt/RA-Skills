## Description:

Email Cron Handler monitors a configured mailbox via IMAP/SMTP, filters command emails from a whitelisted sender, and returns execution results by email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pebblerwon](https://clawhub.ai/user/pebblerwon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect scheduled mailbox monitoring to agent work, where messages from an approved sender can trigger tasks and receive success, failure, or timeout results by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming email can trigger unattended agent work and unintended side effects.

Mitigation: Use a dedicated mailbox and app password, fail closed unless a verified sender is configured, restrict commands to a small allowlist, and require approval for file access or side effects.

Risk: Email replies can expose sensitive command output, secrets, or detailed errors.

Mitigation: Do not place secrets in prompts or cron payloads, sanitize results before replying, and avoid emailing raw outputs or detailed error traces.

## Reference(s):

- [Email Cron Handler configuration template](references/01-config-template.md)
- [ClawHub skill page](https://clawhub.ai/pebblerwon/skills/email-cron-handler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON-style configuration examples, and Python helper script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mailbox polling instructions, cron payload examples, command-fetch/reply/mark script usage, and email status feedback content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
