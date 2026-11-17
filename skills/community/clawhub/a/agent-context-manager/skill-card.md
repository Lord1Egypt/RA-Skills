## Description:

Agent Context Manager manages reusable Agent Context documents that agents and workflows use for brand guidelines, standard operating procedures, product facts, pricing rules, policies, and other persistent operational knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, fetch, update, archive, clone, and version reusable Agent Context documents for AgentPMT-enabled agents and workflows. It is suited for maintaining shared operating knowledge such as brand voice, SOPs, product catalogs, pricing rules, and policy documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, archive, and restore persistent business context documents used by agents and workflows.

Mitigation: Require clear human approval before create, update, archive, or restore actions, and rely on expected revision checks and version history before changing important documents.

Risk: Document bodies may contain sensitive business context.

Mitigation: Avoid storing secrets or highly confidential material unless the organization has approved AgentPMT for that data.

Risk: Setup examples include unpinned installation commands.

Mitigation: Prefer pinned or reviewed setup installs before using the skill in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/agent-context-manager)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/agent-context-manager)
- [Action schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [guidance, markdown, API Calls, configuration]

**Output Format:** [Markdown guidance with JSON call examples and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected AgentPMT action and can include document lists, document bodies, version metadata, warnings, correction targets, or success booleans.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
