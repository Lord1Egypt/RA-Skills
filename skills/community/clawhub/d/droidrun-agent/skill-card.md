## Description: <br>
DroidRun Portal HTTP/WebSocket/MCP client for controlling Android devices with tap, swipe, screenshot, text input, UI state retrieval, app launch and stop, and related Portal operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxi](https://clawhub.ai/user/hanxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an AI agent or Python client to an Android device running DroidRun Portal, inspect device state, capture screenshots, and perform controlled device actions through HTTP, WebSocket, or MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to control an Android device and view screen or UI state through DroidRun Portal. <br>
Mitigation: Use only with trusted devices and trusted Portal endpoints, keep PORTAL_TOKEN private, and avoid exposing the Portal service publicly. <br>
Risk: Sensitive operations such as APK installation, text entry, port changes, or screenshots can disclose private information or change device state. <br>
Mitigation: Require explicit human confirmation before sensitive actions and review device context before executing commands. <br>


## Reference(s): <br>
- [Droidrun Agent on ClawHub](https://clawhub.ai/hanxi/droidrun-agent) <br>
- [Publisher profile](https://clawhub.ai/user/hanxi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, shell, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe Portal API calls, MCP server setup, environment variables, and Android device-control workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
