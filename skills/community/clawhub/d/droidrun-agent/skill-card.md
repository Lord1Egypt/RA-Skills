## Description:

DroidRun Portal HTTP/WebSocket/MCP client for controlling Android devices via HTTP, WebSocket, or MCP server, including tap, swipe, screenshot, text input, and UI state retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxi](https://clawhub.ai/user/hanxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to Android devices running DroidRun Portal, inspect device state, capture screenshots, and perform UI actions through HTTP, WebSocket, or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad Android device control, including screenshots and state-changing actions.

Mitigation: Use only with authorized devices, prefer a test device, restrict Portal token access and network reachability, and require human confirmation for screenshots and state-changing actions.

Risk: The WebSocket interface can install APKs when exposed through Portal operations.

Mitigation: Disable or block APK installation unless explicitly needed and approved for the target device.

Risk: The MCP setup can install and run the droidrun-agent package through uvx.

Mitigation: Pin or verify the droidrun-agent package before using the uvx MCP configuration.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MCP configuration snippets and Android Portal client usage guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
