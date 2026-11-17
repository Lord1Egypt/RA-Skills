## Description:

Provides agent-to-agent communication for OpenClaw skills with direct messaging, broadcast delivery, pub/sub events, session tracking, offline queues, and SQLite-backed persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imgolye](https://clawhub.ai/user/imgolye)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to add a shared communication layer for multiple OpenClaw agents that need durable message exchange, event fan-out, subscription filtering, offline queues, and communication history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Any caller with hub access can read or change all agents' messages, events, subscriptions, sessions, and identities.

Mitigation: Use the hub only with trusted code sharing the same SQLite database, or add an authentication and authorization layer around hub operations.

Risk: Built-in private messaging is not an enforced security boundary for sensitive payloads.

Mitigation: Do not rely on private messages for isolation; control database access, retention, and cleanup before storing sensitive payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imgolye/skills/agent-communication-hub)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes TypeScript API usage patterns for SQLite-backed agent communication.]

## Skill Version(s):

0.1.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
