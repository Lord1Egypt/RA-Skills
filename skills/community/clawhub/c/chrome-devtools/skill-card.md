## Description: <br>
Uses Chrome DevTools via MCP to support web page debugging, browser automation, performance analysis, and network request inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[podcasting101](https://clawhub.ai/user/podcasting101) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent to Chrome DevTools MCP for debugging web pages, automating browser interactions, inspecting page structure, analyzing performance, and troubleshooting network issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server is launched from npm with the floating chrome-devtools-mcp@latest package. <br>
Mitigation: Pin the package version before installation or execution so upgrades are reviewed before use. <br>
Risk: Chrome is configured with --no-sandbox and --disable-setuid-sandbox, which weakens browser isolation. <br>
Mitigation: Remove the no-sandbox flags unless the runtime environment requires them. <br>
Risk: Browser automation can interact with authenticated pages and sensitive browser state. <br>
Mitigation: Use a dedicated low-privilege Chrome profile and avoid logging into sensitive accounts. <br>


## Reference(s): <br>
- [Chrome DevTools documentation](https://developer.chrome.com/docs/devtools) <br>
- [Chrome DevTools AI assistance documentation](https://developer.chrome.com/docs/devtools/ai-assistance) <br>
- [Chrome DevTools MCP troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline command and MCP tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request file outputs for screenshots, snapshots, or traces through MCP filePath parameters.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
