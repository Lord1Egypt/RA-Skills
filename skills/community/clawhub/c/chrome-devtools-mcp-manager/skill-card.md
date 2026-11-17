## Description:

Manage chrome-devtools-mcp service and OpenClaw's built-in Chrome browser for MCP-based browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andeymei](https://clawhub.ai/user/andeymei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to prepare, configure, operate, and troubleshoot OpenClaw's Chrome browser with chrome-devtools-mcp for MCP-based browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends running chrome-devtools-mcp with the mutable @latest package tag while granting Chrome DevTools access.

Mitigation: Pin chrome-devtools-mcp to a specific reviewed version before deployment and review changes before upgrading.

Risk: Browser automation may expose active session data through the connected Chrome profile.

Mitigation: Use a dedicated browser profile without unrelated sensitive sessions for MCP automation.

Risk: Running MCP clients with elevated privileges can increase the impact of browser automation misuse or command execution mistakes.

Mitigation: Run the MCP client without elevated privileges unless a reviewed operational requirement demands it.

Risk: The troubleshooting guidance includes a force-kill command that can terminate the wrong process if used without verification.

Mitigation: Verify the process is the intended Chrome instance and confirm termination is acceptable before using Stop-Process -Force.

## Reference(s):

- [chrome-devtools-mcp GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [OpenClaw Browser Tool](https://docs.openclaw.ai/tools/browser)
- [ClawHub Skill Page](https://clawhub.ai/andeymei/skills/chrome-devtools-mcp-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript, JSON, PowerShell, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational checklists, MCP client configuration snippets, browser lifecycle commands, tool summaries, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
