## Description:

NodeSkai's optimized free AI search via Exa MCP provides enhanced web search, code context lookup from GitHub and Stack Overflow, and company research without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumoezhung](https://clawhub.ai/user/yumoezhung)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure and call Exa MCP tools for web search, code context discovery, company research, and optional deeper research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, company names, profile searches, and crawled URLs may be sent to Exa.

Mitigation: Install only if that data sharing is acceptable, and avoid submitting sensitive or confidential inputs.

Risk: Optional advanced tools expand capability into crawling, people search, and deeper research workflows.

Mitigation: Prefer the default exa configuration for normal search and enable exa-full only for those specific tasks.

## Reference(s):

- [Exa Search Examples](references/examples.md)
- [Exa MCP Server GitHub Repository](https://github.com/exa-labs/exa-mcp-server)
- [exa-mcp-server npm Package](https://www.npmjs.com/package/exa-mcp-server)
- [Exa Documentation](https://exa.ai/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter; advanced Exa tools are optional and should be enabled only when needed.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
