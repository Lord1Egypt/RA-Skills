## Description:

Control Android devices from AI agents using the Another MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfinix](https://clawhub.ai/user/zfinix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and testers use this skill to inspect, control, test, and automate Android devices through the Another MCP server, including screenshots, touch input, text entry, app launching, shell commands, and WiFi debugging setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can view Android screenshots that may contain private data.

Mitigation: Prefer a test device or emulator, and avoid opening screens, accounts, or apps that contain sensitive data.

Risk: Touch input, text entry, app launching, and button presses can change device state.

Mitigation: Require human approval for actions that affect accounts, apps, files, settings, or purchases, and verify important actions with screenshots before and after execution.

Risk: ADB shell commands and WiFi debugging can alter settings, apps, files, accounts, or network/debugging state.

Mitigation: Require explicit approval before shell commands or WiFi debugging changes, and use disposable devices or emulators for higher-risk automation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active Another MCP server and an Android device or emulator available through ADB.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
