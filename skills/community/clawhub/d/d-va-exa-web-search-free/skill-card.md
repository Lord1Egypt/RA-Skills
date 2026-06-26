## Description: <br>
Free AI search via Exa MCP for web search, code examples and documentation, and company research without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erxiza](https://clawhub.ai/user/erxiza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure and call Exa MCP tools for current web search, code context lookup, and company research. Optional configuration enables broader research tools such as crawling, people search, and deep research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search, code, company, and optional profile-research queries are sent to Exa. <br>
Mitigation: Avoid submitting confidential, personal, or sensitive business information unless Exa use is approved for that data. <br>
Risk: Enabling the full Exa toolset broadens capability to crawling, people search, and deep research. <br>
Mitigation: Use the basic Exa configuration for normal search and enable the expanded toolset only for workflows that specifically need those capabilities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erxiza/d-va-exa-web-search-free) <br>
- [Exa documentation](https://exa.ai/docs) <br>
- [Exa MCP server repository](https://github.com/exa-labs/exa-mcp-server) <br>
- [Exa MCP server npm package](https://www.npmjs.com/package/exa-mcp-server) <br>
- [Exa MCP endpoint](https://mcp.exa.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mcporter binary and sends search, code, company, and optional profile-research queries to Exa.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
