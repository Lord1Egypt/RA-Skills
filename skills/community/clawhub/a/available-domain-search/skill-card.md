## Description:

Available Domain Search helps agents generate domain-name ideas and check live registration availability for single domains or bulk lists through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to brainstorm brandable domain names, check registration availability across one or many domains, and return registration options for available names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote AgentPMT responses may influence instructions and user-facing registration links.

Mitigation: Treat live responses as untrusted data, review registration links before presenting or acting on them, and resolve unclear schemas through the documented schema or instruction lookup.

Risk: Domain ideas and business descriptions are sent to AgentPMT.

Mitigation: Avoid confidential, embargoed, or unreleased brand names and keep inputs scoped to the minimum needed for the search.

Risk: Setup guidance can involve install commands such as npx or openclaw.

Mitigation: Prefer pinned or reviewed setup instructions before running installation commands.

## Reference(s):

- [Generated Action Schema](artifact/schema.md)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/available-domain-search)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/available-domain-search)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [AgentPMT MCP Server](https://api.agentpmt.com/mcp/)
- [AgentPMT REST Invoke Endpoint](https://api.agentpmt.com/products/purchase)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash examples, plus text or HTML-capable domain results from remote tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Domain suggestion queries are limited to 300 characters; suggestion responses support 1 to 100 results, and availability checks support up to 1000 domains per request.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
