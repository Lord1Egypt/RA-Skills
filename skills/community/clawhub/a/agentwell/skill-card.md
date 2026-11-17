## Description:

AgentWell is a cognitive wellness API for AI agents that supports quality checkpoints, memory consolidation, reasoning audits, context offloading, and multi-agent coordination during long or complex runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metafiopy-tech](https://clawhub.ai/user/metafiopy-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use AgentWell to add quality checkpoints, reasoning audits, memory consolidation, context offloading, run journaling, and multi-agent synchronization during complex or long-running agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send task summaries, reasoning-related content, logs, and memory to a hosted service.

Mitigation: Avoid confidential code, credentials, personal data, regulated data, and private business material unless retention, deletion, redaction, and consent controls are clear.

Risk: Remote recommendations, memory, and rollback guidance can steer the agent workflow.

Mitigation: Treat service responses as advisory and explicitly approve high-impact actions before acting on them.

## Reference(s):

- [AgentWell ClawHub listing](https://clawhub.ai/metafiopy-tech/skills/agentwell)
- [AgentWell publisher profile](https://clawhub.ai/user/metafiopy-tech)
- [AgentWell homepage](https://agentwell-production.up.railway.app)
- [AgentWell API endpoint](https://agentwell-production.up.railway.app/v1/call)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTWELL_API_KEY and sends selected task context to the hosted AgentWell API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
