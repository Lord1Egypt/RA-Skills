## Description:

Free AI search via Exa MCP for web search, code examples, documentation lookup, and company research without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15914355527](https://clawhub.ai/user/15914355527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure and call Exa MCP search tools for current web information, code context, company research, and optional deeper research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, company or person lookups, and crawled URLs may be sent to Exa's remote MCP service.

Mitigation: Use the skill only for queries and URLs that are appropriate to share with the Exa service.

Risk: The optional expanded endpoint enables additional deep search, crawling, people search, and research-agent tools.

Mitigation: Enable the optional full tool set only when those added capabilities are needed.

## Reference(s):

- [Exa Search Examples](references/examples.md)
- [Exa MCP Server on GitHub](https://github.com/exa-labs/exa-mcp-server)
- [exa-mcp-server npm Package](https://www.npmjs.com/package/exa-mcp-server)
- [Exa Documentation](https://exa.ai/docs)
- [ClawHub Skill Page](https://clawhub.ai/15914355527/skills/exa-web-search-v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can configure the core Exa MCP endpoint or an optional expanded endpoint with additional tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
