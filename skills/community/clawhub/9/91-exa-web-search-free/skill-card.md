## Description:

Free AI search via Exa MCP for web search, code examples, documentation lookup, and company research without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and call Exa MCP search tools for current web information, code and documentation examples, company research, and optional advanced research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, URLs, company names, and people-search terms are sent to Exa's external MCP service.

Mitigation: Do not include secrets, credentials, confidential business information, or sensitive personal information in queries.

Risk: Optional advanced tools expand the amount and sensitivity of research activity, including crawling, people search, and deep research workflows.

Mitigation: Enable the advanced tool bundle only when those tools are needed for the task.

## Reference(s):

- [Exa Search Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/91-exa-web-search-free)
- [Exa MCP server on GitHub](https://github.com/exa-labs/exa-mcp-server)
- [exa-mcp-server on npm](https://www.npmjs.com/package/exa-mcp-server)
- [Exa documentation](https://exa.ai/docs)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mcporter configuration and call patterns for Exa MCP tools; advanced tools are optional.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
