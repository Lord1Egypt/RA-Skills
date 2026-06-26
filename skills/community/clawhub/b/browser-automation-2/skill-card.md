## Description: <br>
Control Chrome browser with AI using MCP protocol to automate navigation, screenshots, form filling, content extraction, history, bookmark, and network tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[femto](https://clawhub.ai/user/femto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and MCP-compatible agent users use this skill to connect an AI client to an existing Chrome browser session for web navigation, page inspection, screenshots, form interaction, history search, bookmark management, and network monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an AI client broad access to a real logged-in Chrome browser. <br>
Mitigation: Use a dedicated Chrome profile and avoid sensitive logged-in accounts unless the task requires them. <br>
Risk: Browser history, network traffic, screenshots, cookies, form submissions, bookmarks, and account data may expose private or security-sensitive information. <br>
Mitigation: Require explicit confirmation before reading history, capturing network traffic, sending cookie-backed requests, submitting forms, deleting bookmarks, posting content, or changing account data. <br>
Risk: The skill depends on an upstream npm bridge and Chrome extension. <br>
Mitigation: Install only from trusted upstream sources, and pin and verify the npm package and extension release where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/femto/browser-automation-2) <br>
- [mcp-chrome GitHub repository](https://github.com/femto/mcp-chrome) <br>
- [mcp-chrome releases](https://github.com/femto/mcp-chrome/releases) <br>
- [mcp-chrome-bridger npm package](https://www.npmjs.com/package/mcp-chrome-bridger) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Screenshots] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and browser automation tool names.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on the user's active Chrome profile, open tabs, login sessions, bookmarks, history, and browser extension state.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
