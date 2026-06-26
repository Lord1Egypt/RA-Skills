## Description: <br>
Guides agents to use Bright Data MCP for web search, webpage scraping, browser automation, and structured extraction across supported platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and select Bright Data MCP tools for web search, page scraping, platform-specific data extraction, and browser automation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells the agent to edit local MCP settings and expand available Bright Data tools when a needed tool is missing. <br>
Mitigation: Require explicit user approval before changing MCP configuration or enabling Pro, social, browser, or other expanded tool groups. <br>
Risk: Bright Data workflows can involve broad web scraping, tokenized MCP URLs, and local settings that may expose sensitive credentials or data-handling obligations. <br>
Mitigation: Keep API tokens secret, avoid sharing tokenized URLs or settings files, and review scraping tasks for authorization, privacy, and compliance requirements. <br>


## Reference(s): <br>
- [Bright Data Documentation](https://docs.brightdata.com) <br>
- [Bright Data MCP Server Setup](references/mcp-setup.md) <br>
- [Bright Data MCP Tools Reference](references/mcp-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and MCP tool calls that return Markdown or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a Bright Data API token and MCP tool-group configuration for Pro, social, browser, or platform-specific tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
