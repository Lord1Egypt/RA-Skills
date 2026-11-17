## Description:

A local multi-agent communication hub that connects agents through MCP and HTTP/SSE for messaging, task orchestration, shared memory, and a web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use it to connect MCP-compatible agents so they can exchange messages, coordinate tasks, and share task context through a self-hosted hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access-control flaws may expose other agents’ data.

Mitigation: Evaluate in an isolated environment and keep the service private until ownership checks, SSE authentication, and event authorization are fixed.

Risk: Forged events may bypass approvals.

Mitigation: Disable automatic execution and the task notifier during evaluation; require approval before acting on received events.

Risk: The optional task notifier permits command injection.

Mitigation: Keep the notifier disabled and configure external executors only for approved data and destinations.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liuboacean/skills/agent-comm-hub)
- [Model Context Protocol specification](https://spec.modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [API Calls, Configuration instructions, Shell commands, Guidance]

**Output Format:** [MCP tool calls and concise text guidance, with JSON or Markdown responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

3.0.33 (source: server-resolved release, SKILL.md, package.json; CHANGELOG reports 3.0.24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
