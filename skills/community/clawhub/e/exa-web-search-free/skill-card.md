## Description:

Free AI search via Exa MCP. Web search for news/info, code search for docs/examples from GitHub/StackOverflow, company research for business intel. No API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whiteknight07](https://clawhub.ai/user/whiteknight07)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to configure and call Exa MCP search tools for current web information, code/documentation lookup, and company research. It also documents optional broader Exa tools for advanced web search, crawling, people search, and deep research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and retrieved context may be sent to a third-party Exa MCP service.

Mitigation: Use the skill only with information policy permits sending to Exa; avoid secrets, proprietary source code, personal data, and sensitive business research.

Risk: The optional all-tools configuration persistently enables broader crawling, people search, and deep researcher capabilities.

Mitigation: Enable only the specific Exa tools needed for the task, and keep advanced tools disabled unless their use has been reviewed.

Risk: Search and research results can be incomplete, stale, or misleading.

Mitigation: Review important outputs against authoritative sources before using them for decisions or downstream actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whiteknight07/skills/exa-web-search-free)
- [Exa MCP server GitHub repository](https://github.com/exa-labs/exa-mcp-server)
- [exa-mcp-server npm package](https://www.npmjs.com/package/exa-mcp-server)
- [Exa documentation](https://exa.ai/docs)
- [Exa Search Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and an Exa MCP server configuration; no API key is documented as required.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
