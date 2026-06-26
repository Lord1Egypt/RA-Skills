## Description: <br>
Free AI search via Exa MCP for web and news lookup, code examples, documentation, and company research without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15914355527](https://clawhub.ai/user/15914355527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to configure and call Exa MCP search tools for current web information, code context, documentation examples, company research, and optional deeper search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, company names, and people-search terms are sent to Exa's remote MCP service. <br>
Mitigation: Avoid submitting secrets, private source code, internal URLs, confidential business topics, regulated personal data, or sensitive people-search queries unless approved. <br>
Risk: Optional advanced tools expand the data sent to Exa through crawling, people search, and deeper research workflows. <br>
Mitigation: Use the default Exa configuration for ordinary search and enable exa-full only when the advanced tools are intentionally required. <br>


## Reference(s): <br>
- [Exa Search Examples](references/examples.md) <br>
- [Exa MCP Server GitHub](https://github.com/exa-labs/exa-mcp-server) <br>
- [Exa MCP Server npm](https://www.npmjs.com/package/exa-mcp-server) <br>
- [Exa Documentation](https://exa.ai/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/15914355527/exa-web-search-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on mcporter commands and Exa MCP tool calls; remote responses may include web, code, company, crawl, people-search, or research-agent results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
