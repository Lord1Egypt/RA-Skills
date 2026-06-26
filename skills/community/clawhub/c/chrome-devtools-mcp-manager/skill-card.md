## Description: <br>
Manage chrome-devtools-mcp service and OpenClaw's built-in Chrome browser for MCP-based browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andeymei](https://clawhub.ai/user/andeymei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to prepare, configure, and troubleshoot OpenClaw's built-in Chrome browser with chrome-devtools-mcp for MCP-based browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP-based browser automation can control browser pages and inspect browser state. <br>
Mitigation: Use this skill only when browser automation is intended, and avoid sensitive logged-in pages unless required. <br>
Risk: Using chrome-devtools-mcp@latest can install an unpinned package version. <br>
Mitigation: Pin chrome-devtools-mcp to a trusted version before routine or sensitive use. <br>
Risk: The force-kill troubleshooting command can terminate the wrong process if port 18800 is owned by something unexpected. <br>
Mitigation: Verify the process name and path owning port 18800 before running any force-kill command. <br>


## Reference(s): <br>
- [Chrome DevTools MCP Manager on ClawHub](https://clawhub.ai/andeymei/chrome-devtools-mcp-manager) <br>
- [chrome-devtools-mcp GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) <br>
- [OpenClaw Browser Tool](https://docs.openclaw.ai/tools/browser) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with command examples, JSON configuration snippets, and JavaScript browser-tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes status checks, setup workflows, MCP client configuration, and troubleshooting commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
