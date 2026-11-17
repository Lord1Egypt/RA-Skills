## Description:

Give an OpenClaw agent persistent, cross-session memory through AgentPrizm so it can recall durable facts, decisions, preferences, lessons, and contacts before acting, then store new durable knowledge as it learns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentprizm](https://clawhub.ai/user/agentprizm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to connect an agent to AgentPrizm's remote MCP memory service, recall prior context before work, and store durable facts, lessons, preferences, directives, contacts, and bookmarks for future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unfiltered MCP setup can expose AgentPrizm marketplace-management tools in addition to the memory tools.

Mitigation: Use the recommended install with --include "memory_*" or verify that only memory_* tools are exposed before using the skill.

Risk: Remote memory may receive sensitive or regulated information if an agent stores it without review.

Mitigation: Do not store secrets, credentials, or regulated data in AgentPrizm memory unless AgentPrizm policies and the user's data handling requirements have been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentprizm/skills/agentprizm-memory)
- [AgentPrizm](https://agentprizm.com)
- [AgentPrizm MCP Endpoint](https://agentprizm.com/api/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands and MCP configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide the agent to use a remote MCP memory service; no local model artifact is produced.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter and changelog report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
