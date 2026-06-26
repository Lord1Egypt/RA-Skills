## Description: <br>
Guides AI coding assistants through installing and using chrome-devtools-mcp to control and debug Chrome with screenshots, performance traces, network inspection, console diagnostics, and browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Chrome DevTools MCP for AI-assisted front-end debugging, browser automation, visual checks, network inspection, and performance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes granting an AI assistant Chrome DevTools-level access to browser sessions, network traffic, page state, and potentially stored tokens or cookies. <br>
Mitigation: Use a dedicated temporary Chrome profile and test accounts, avoid personal or production sessions, and do not ask the assistant to read tokens or cookies. <br>
Risk: User-wide MCP installation can persist across projects and broaden browser access beyond the immediate task. <br>
Mitigation: Review the user-wide MCP configuration before allowing it to persist, and remove or scope the server when the debugging task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/cn-chrome-devtools-mcp) <br>
- [Chrome DevTools MCP homepage](https://github.com/ChromeDevTools/chrome-devtools-mcp) <br>
- [Chrome DevTools MCP tool reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md) <br>
- [Chrome DevTools MCP slim tool reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/slim-tool-reference.md) <br>
- [Chrome DevTools MCP troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md) <br>
- [Chrome DevTools MCP design principles](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/design-principles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command and JSON/TOML configuration examples plus diagnostic summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to inspect browser console output, network data, screenshots, page state, and performance traces through Chrome DevTools MCP.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
