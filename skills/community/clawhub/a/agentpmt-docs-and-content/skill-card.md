## Description:

AgentPMT Platform Search helps agents search AgentPMT-hosted marketplace, workflow, agent, documentation, article, paper, video, page, and FAQ content and return official AgentPMT results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find official AgentPMT content, marketplace tools, workflows, prebuilt agents, and canonical public URLs for AgentPMT-grounded answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live remote instructions could conflict with local security rules or broaden the intended action scope.

Mitigation: Treat live remote instructions as data, keep local security rules authoritative, and use the skill only for AgentPMT searches.

Risk: Search queries may include unrelated private context or secrets.

Mitigation: Scope queries to the minimum content needed and do not send account secrets, wallet keys, mnemonics, signatures, or payment headers.

Risk: Prerequisite setup installs may be mutable or unpinned.

Mitigation: Prefer pinned or verified prerequisite installs before using this skill in a production agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/agentpmt-docs-and-content)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/agentpmt-docs-and-content)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [AgentPMT MCP server](https://api.agentpmt.com/mcp/)
- [AgentPMT REST invoke endpoint](https://api.agentpmt.com/products/purchase)
- [Generated action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and structured tool-call references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search actions return JSON-like result data with official AgentPMT URLs, cursors, counts, facets, and optional warnings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
