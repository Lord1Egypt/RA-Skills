## Description:

Clawback is a Gmail security proxy with policy enforcement, approval workflows, and audit logging for agents that read, search, or send Gmail with guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rotemtam](https://clawhub.ai/user/rotemtam)

### License/Terms of Use:

Apache-2.0

## Use Case:

Employees, external users, and developers use this skill to let an agent search, inspect, compose, and send Gmail through Clawback guardrails, approvals, policy checks, and audit logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact mailbox actions such as deletes, batch modifies, label changes, and draft actions without explicit confirmation guidance beyond sending email.

Mitigation: Require a clear preview and explicit user confirmation before deletes, batch modifications, label changes, draft actions, and sends.

Risk: The skill requires a local Clawback CLI and Gmail service access, so mailbox data and actions depend on trusting that CLI and service.

Mitigation: Install only a trusted Clawback CLI, verify the configured service before authentication, and rely on organization policy controls and audit logs for sensitive accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rotemtam/skills/clawback-sh)
- [Clawback homepage](https://clawback.sh)
- [Clawback CLI releases](https://github.com/honeybadge-labs/clawback/releases)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to prefer JSON CLI output for reliable parsing and to present sensitive email actions to users in plain language.]

## Skill Version(s):

0.2.0 (source: evidence.release.version, package.json, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
