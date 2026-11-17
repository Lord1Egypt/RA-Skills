## Description:

Multi-worker orchestration for Claude Code with Notion visibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theagentacademy](https://clawhub.ai/user/theagentacademy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage multiple Claude Code workers, route tasks between them, preserve worker sessions, and inspect orchestration status through a local HTTP API with Notion visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The orchestrator can control Claude sessions and persist worker context.

Mitigation: Run it in a dedicated low-privilege environment and review what session data is stored before using it with sensitive work.

Risk: The skill depends on mutable external code and package installation.

Mitigation: Install only from a pinned, audited commit or release and review dependency changes before upgrades.

Risk: External integrations may sync context or notifications to Notion or Telegram.

Mitigation: Use least-privilege Notion credentials and avoid sending secrets or proprietary code unless the persistence and sync behavior is acceptable.

Risk: The local HTTP API can spawn, route, suspend, and resume workers.

Mitigation: Keep the API bound to localhost and add access controls before exposing it beyond the local machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theagentacademy/skills/agent-relay-orchestrator)
- [Publisher profile](https://clawhub.ai/user/theagentacademy)
- [Project homepage](https://github.com/TheAgentAcademy/agent-relay-orchestrator)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and curl code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume a local Agent Relay Orchestrator service, Claude Code CLI, Node.js, and configured Notion credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
