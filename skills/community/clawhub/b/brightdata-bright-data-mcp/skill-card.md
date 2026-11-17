## Description:

Bright Data MCP guides an agent to use Bright Data MCP tools for web search, webpage retrieval, structured platform data extraction, and browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route web data tasks through Bright Data MCP, including search, page scraping, structured data collection, and browser automation. It is useful when an agent needs guidance for selecting Bright Data MCP tools and configuring available tool groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill reroutes all web activity through Bright Data.

Mitigation: Review before installing and use it only when sending web queries and URLs to Bright Data is acceptable.

Risk: The security review says the skill asks the agent to modify MCP settings to unlock more tools without prior approval.

Mitigation: Require explicit user approval before editing MCP settings or enabling Pro tool groups.

Risk: MCP configuration can expose or misuse service tokens.

Mitigation: Use manual, scoped setup with protected tokens and pinned local package versions.

## Reference(s):

- [Bright Data documentation](https://docs.brightdata.com)
- [MCP setup](references/mcp-setup.md)
- [MCP tools reference](references/mcp-tools.md)
- [ClawHub skill page](https://clawhub.ai/meirk-brd/skills/brightdata-bright-data-mcp)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to invoke external MCP tools that return Markdown or JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
