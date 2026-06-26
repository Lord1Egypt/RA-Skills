## Description: <br>
Domain expertise for Ai2 Asta MCP tools (Semantic Scholar corpus). Intent-to-tool routing, safe defaults, workflow patterns, and pitfall warnings for academic paper search, citation traversal, and author discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route academic literature questions to Ai2 Asta MCP tools for paper search, citation traversal, author discovery, and evidence retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes academic-paper queries to an external Asta MCP service using a user-provided API key. <br>
Mitigation: Configure ASTA_API_KEY only in a trusted host and avoid sending private or sensitive research queries unless the user accepts sharing them with the external service. <br>
Risk: Large citation or reference fields can exceed an agent context window or trigger rate limits. <br>
Mitigation: Use safe default fields, prefer the paginated citations tool for citation traversal, batch lookups when possible, and stop expanding graphs beyond the requested scope. <br>
Risk: Academic corpus metadata can be missing, ambiguous, or best-effort for external identifiers. <br>
Mitigation: Disambiguate authors and papers before lookup, report missing abstract or venue fields plainly, and degrade gracefully when external identifiers are unavailable. <br>


## Reference(s): <br>
- [ClawHub listing for Asta Skill](https://clawhub.ai/agents365-ai/asta-skill) <br>
- [Asta MCP endpoint](https://asta-tools.allen.ai/mcp/v1) <br>
- [Asta API key request](https://share.hsforms.com/1L4hUh20oT3mu8iXJQMV77w3ioxm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with tool-routing tables and workflow patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an MCP-capable host configured with ASTA_API_KEY for Asta MCP access.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
