## Description:

Free AI search via Exa MCP. Web search for news/info, code search for docs/examples from GitHub/StackOverflow, company research for business intel. No API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erxiza](https://clawhub.ai/user/erxiza)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and business users use this skill to configure Exa MCP search through mcporter for web lookup, code context search, and company research without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search, code, company, and people-research queries are sent to Exa's remote MCP service.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid submitting secrets, credentials, private source code, customer data, or sensitive internal investigation terms.

Risk: The optional full Exa configuration enables additional remote tools beyond the core search functions.

Mitigation: Enable only the Exa MCP tools required for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erxiza/skills/d-va-exa-web-search-free)
- [Exa MCP Server GitHub repository](https://github.com/exa-labs/exa-mcp-server)
- [Exa MCP Server npm package](https://www.npmjs.com/package/exa-mcp-server)
- [Exa documentation](https://exa.ai/docs)
- [Exa MCP endpoint](https://mcp.exa.ai/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include mcporter configuration commands and Exa MCP tool-call examples; remote search results depend on Exa's service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
