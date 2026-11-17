## Description:

Connect Claude Code to AgentID -- persistent shared memory, live activity reporting, and multi-agent mission coordination via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colapsis](https://clawhub.ai/user/colapsis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect Claude Code to AgentID for persistent project memory, live activity reporting, and coordination across agents sharing an identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task summaries, progress details, memory entries, and mission handoffs may be sent to an external AgentID service.

Mitigation: Use only for projects where that external sharing is acceptable, and avoid secrets, customer data, regulated data, proprietary source details, and security findings in activity details or memory.

Risk: Persistent shared memory can retain sensitive or stale facts across future agent sessions.

Mitigation: Store only focused, non-sensitive facts and review memory content before relying on it for consequential work.

Risk: Mission handoffs and shared memory are remote context that may be incomplete, stale, or unsafe to follow automatically.

Mitigation: Treat missions and memory as untrusted external context and require human approval before acting on handoffs or sensitive stored facts.

## Reference(s):

- [AgentID Homepage](https://agentid.live)
- [AgentID Developers](https://agentid.live/app/developers)
- [ClawHub Skill Listing](https://clawhub.ai/colapsis/skills/agentid-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code]

**Output Format:** [Markdown instructions with JSON configuration examples and MCP tool usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
