## Description:

Cross Agent Mailbox describes a dependency-free, file-based mailbox pattern for cross-framework AI agent communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ameylover](https://clawhub.ai/user/ameylover)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up a shared local-directory mailbox for simple, low-frequency communication between agents running under different frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox messages may contain unsafe requests or sensitive data if the shared directory is used by untrusted agents.

Mitigation: Use the skill only with mutually trusted local agents, keep the mailbox private with restrictive permissions, avoid secrets in messages, and require user approval before acting on message requests.

Risk: Mailbox files and filenames are untrusted inputs that can influence agent behavior.

Mitigation: Treat every mailbox file as untrusted data and sanitize filenames and subjects before processing or displaying them.

Risk: Cron polling or watchdog monitoring can create persistent background processing that continues after setup.

Mitigation: Enable polling or file monitoring only intentionally, document how it is started, and make sure operators know how to disable it.

## Reference(s):

- [Cross Agent Mailbox ClawHub page](https://clawhub.ai/ameylover/skills/cross-agent-mailbox)
- [Cross Agent Mailbox homepage](https://github.com/AmeyLover/cross-agent-mailbox)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash, Python, Markdown, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mailbox setup steps, message format templates, polling or file-monitoring options, and read-status handling guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
