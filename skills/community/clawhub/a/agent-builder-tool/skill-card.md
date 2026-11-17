## Description:

Agent Builder Tool creates, configures, publishes, and manages custom AI agents end to end through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and teams use this skill to create and manage AgentPMT agents, including drafts, remixes, tools, workflows, context documents, publishing, archiving, and showcase chat examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent creation and updates may send prompts, context document IDs, workflow choices, and tool selections to the AgentPMT remote service.

Mitigation: Review the payload before each call and keep submitted account data, prompts, and document references limited to what the task requires.

Risk: Publishing, archiving, remixing, and composition actions can change agent state or attach tools and workflows.

Mitigation: Confirm the target agent ID or slug, requested action, and redirect path before execution, and prefer dedicated publish or archive actions over direct status edits.

Risk: Setup examples include unpinned npx installation commands.

Mitigation: Prefer pinned or ClawHub-reviewed setup paths when installing companion skills or preparing production integrations.

## Reference(s):

- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/agent-builder-tool)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/agent-builder-tool)
- [Agent Builder Tool Schema](schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions, JSON, Shell commands]

**Output Format:** [Markdown with JSON request examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include AgentPMT action names, request shapes, response handling guidance, setup references, and risk-aware usage notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
