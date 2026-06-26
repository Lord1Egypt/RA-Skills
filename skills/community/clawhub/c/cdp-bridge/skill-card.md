## Description: <br>
CDP Bridge MCP Browser Control helps an agent operate a real browser through the CDP Bridge extension, including tab listing, page scanning, JavaScript execution, screenshots, navigation, waits, batch CDP commands, and cookie reads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miyan1221](https://clawhub.ai/user/miyan1221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to control an installed, real browser session through a local CDP Bridge MCP service. It is intended for browser inspection and automation tasks such as reading page content, switching tabs, executing JavaScript, taking screenshots, navigating pages, waiting for page conditions, and reading cookies when explicitly appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a live logged-in browser and access page data, cookies, screenshots, and JavaScript execution. <br>
Mitigation: Use a separate browser profile, avoid sensitive accounts, and approve cookie reads, screenshots, and page-data access only for a specific site and purpose. <br>
Risk: JavaScript execution, navigation, and batch CDP commands can change state in the active browser session. <br>
Mitigation: Review JavaScript, navigation targets, and batch actions before running them, and confirm the target tab with browser_get_tabs first. <br>
Risk: The server security summary marks the release as needing review because consent boundaries for browser control are not clear. <br>
Mitigation: Review and scan the skill before deployment, and require explicit user approval for browser-control actions that expose or alter sensitive state. <br>


## Reference(s): <br>
- [CDP Bridge MCP API calling guide](references/cdp-bridge-api.md) <br>
- [CDP Bridge tool parameters](references/cdp-bridge-tools.md) <br>
- [CDP Bridge operation examples](references/cdp-bridge-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/miyan1221/cdp-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls, Code] <br>
**Output Format:** [Markdown guidance with PowerShell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may guide browser-control calls that return JSON text, page data, cookies, or base64 PNG screenshots from the underlying MCP tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
