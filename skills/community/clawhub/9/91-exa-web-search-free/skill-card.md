## Description: <br>
Free AI search via Exa MCP for web search, code and documentation lookup, and company research without a user-supplied API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to configure and call Exa MCP search tools for current web information, code examples, documentation, and company research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, company names, and people-search queries are sent to an external Exa service. <br>
Mitigation: Do not submit secrets, private source code, internal-only URLs, customer records, regulated data, or sensitive personal information. <br>
Risk: Optional people search, crawling, and deep research tools can expand collection or retrieval beyond basic search. <br>
Mitigation: Use optional advanced tools only with appropriate permission and compliance clearance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/91-exa-web-search-free) <br>
- [Exa Search Examples](references/examples.md) <br>
- [Exa MCP Server GitHub Repository](https://github.com/exa-labs/exa-mcp-server) <br>
- [Exa MCP Server npm Package](https://www.npmjs.com/package/exa-mcp-server) <br>
- [Exa Documentation](https://exa.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and sends search queries, URLs, company names, and optional people-search queries to an external Exa service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
