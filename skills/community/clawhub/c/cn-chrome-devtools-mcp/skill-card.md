## Description:

Guides agents to install and use Chrome DevTools MCP so they can control and debug a real Chrome browser for screenshots, console inspection, network analysis, performance tracing, and browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure an AI coding assistant with Chrome DevTools MCP and run browser-based debugging workflows against local or remote web pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad AI-assisted control over Chrome, including page navigation, JavaScript execution, screenshots, console inspection, and network inspection.

Mitigation: Use a dedicated disposable browser profile and avoid personal or production logged-in sessions.

Risk: The artifact recommends unpinned runtime installation with @latest.

Mitigation: Pin chrome-devtools-mcp to a reviewed npm package version before deployment.

Risk: The artifact includes an example that reads a user token from localStorage.

Mitigation: Do not ask the agent to read tokens, cookies, authorization headers, or other secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/skills/cn-chrome-devtools-mcp)
- [Chrome DevTools MCP project homepage](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Chrome DevTools MCP tool reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md)
- [Chrome DevTools MCP slim tool reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/slim-tool-reference.md)
- [Chrome DevTools MCP troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or TOML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to operate Chrome and inspect browser state after the MCP server is configured.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
