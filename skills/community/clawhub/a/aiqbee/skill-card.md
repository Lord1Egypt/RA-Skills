## Description:

Connect to your Aiqbee knowledge graph via MCP. Search, create, and link neurons across your architecture, portfolio, and digital strategy brains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louisgoodier](https://clawhub.ai/user/louisgoodier)

### License/Terms of Use:


## Use Case:

Developers and Aiqbee users use this skill to connect an agent to an Aiqbee knowledge graph, search knowledge records, and create, update, delete, or link neurons and relationships through MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad write access to persistent Aiqbee knowledge-graph records, including creating, updating, deleting, and linking neurons and relationships.

Mitigation: Install only when the agent should have write access to the Aiqbee brain, require explicit confirmation before changes or deletion, and ask the agent to search or preview targets before write actions.

Risk: The security evidence notes no documented confirmation or recovery safeguards for destructive knowledge-graph actions.

Mitigation: Review proposed delete and update operations carefully and keep operational recovery practices outside the skill before using it on important records.

## Reference(s):

- [Aiqbee](https://aiqbee.com)
- [Aiqbee Platform](https://app.aiqbee.com)
- [Aiqbee Documentation](https://app.aiqbee.com/help)
- [Aiqbee MCP Server](https://mcp.aiqbee.com/mcp)
- [Aiqbee GitHub](https://github.com/AIQBee/aiqbee-ai)
- [ClawHub skill page](https://clawhub.ai/louisgoodier/skills/aiqbee)
- [ClawHub publisher profile](https://clawhub.ai/user/louisgoodier)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include MCP tool calls that read, create, update, delete, and link Aiqbee knowledge-graph records.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
