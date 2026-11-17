## Description:

Provides domain expertise for Ai2 Asta MCP tools over the Semantic Scholar corpus, including intent-to-tool routing, safe defaults, workflow patterns, and pitfall warnings for academic paper search, citation traversal, and author discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this skill to route academic search, paper lookup, citation traversal, author discovery, and snippet retrieval requests through an Asta MCP server connected to the Semantic Scholar corpus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Asta MCP calls use ASTA_API_KEY with an external academic-search service.

Mitigation: Store the key securely and install the skill only when the agent is expected to query the Asta MCP endpoint.

Risk: Broad paper fields such as citations or references can return very large responses.

Mitigation: Use the skill's safe default fields and paginated citation workflow before requesting larger paper metadata.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/skills/asta-skill)
- [Asta MCP Endpoint](https://asta-tools.allen.ai/mcp/v1)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with tool names, workflow steps, tables, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an MCP-capable host with the Asta MCP server registered and ASTA_API_KEY available.]

## Skill Version(s):

0.3.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
