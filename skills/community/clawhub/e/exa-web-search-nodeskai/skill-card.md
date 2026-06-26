## Description: <br>
Provides Exa-powered web search, code context lookup, and company research through mcporter with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YumoeZhung](https://clawhub.ai/user/YumoeZhung) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill to search current web information, retrieve code examples and documentation, and collect company research through Exa MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches and optional research actions are sent to Exa's remote MCP service. <br>
Mitigation: Avoid sending secrets, internal-only URLs, confidential company terms, or sensitive personal data in queries. <br>
Risk: The exa-full configuration enables crawling, people search, and long-running remote research tools. <br>
Mitigation: Enable exa-full only when those advanced tools are specifically needed and review tool calls before use. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/YumoeZhung/exa-web-search-nodeskai) <br>
- [Exa Search Examples](references/examples.md) <br>
- [Exa MCP Server GitHub](https://github.com/exa-labs/exa-mcp-server) <br>
- [Exa MCP Server npm Package](https://www.npmjs.com/package/exa-mcp-server) <br>
- [Exa Documentation](https://exa.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and Exa MCP call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter; optional exa-full configuration enables advanced search, crawling, people search, and long-running research tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
