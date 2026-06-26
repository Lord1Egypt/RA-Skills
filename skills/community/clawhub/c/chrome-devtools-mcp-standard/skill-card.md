## Description: <br>
Provides setup and operating guidance for using Chrome DevTools MCP to automate, inspect, debug, and audit web pages through a local Chrome browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lac5q](https://clawhub.ai/user/lac5q) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Chrome DevTools MCP and guide browser automation workflows such as navigation, form interaction, screenshots, console and network inspection, performance tracing, Lighthouse audits, and mobile emulation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables agents to control and inspect a real Chrome browser, including logged-in sites and sensitive page, console, or network content. <br>
Mitigation: Use a separate or isolated Chrome profile and require explicit approval before using logged-in sites, submitting forms, uploading files, changing account or business data, making purchases, or inspecting sensitive content. <br>
Risk: The artifact installs or runs the MCP server through npm commands that may resolve the latest package at execution time. <br>
Mitigation: Pin the npm package version during installation or npx execution when repeatability or supply-chain control matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lac5q/chrome-devtools-mcp-standard) <br>
- [Chrome DevTools MCP GitHub Repository](https://github.com/ChromeDevTools/chrome-devtools-mcp) <br>
- [Chrome DevTools MCP Tool Reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md) <br>
- [Chrome DevTools MCP Slim Mode Reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/slim-tool-reference.md) <br>
- [Chrome DevTools MCP Troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with bash, JSON, and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP server setup snippets, tool-selection guidance, workflow examples, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
