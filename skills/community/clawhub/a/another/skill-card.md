## Description: <br>
Control Android devices from AI agents using the Another MCP server for screen observation, touch and text input, button presses, app launching, shell commands, WiFi debugging, and swipe gestures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfinix](https://clawhub.ai/user/zfinix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, testers, and automation agents use this skill to inspect and control authorized Android devices for interaction, testing, screenshots, and routine device automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad Android device control, including screenshots, touch and text input, app launching, arbitrary ADB shell commands, and WiFi debugging. <br>
Mitigation: Install only when the separate Another desktop app is trusted and the target device is authorized; prefer a test device or test profile. <br>
Risk: Agent access to personal, banking, messaging, account, or enterprise apps could expose sensitive data or perform unintended actions. <br>
Mitigation: Keep sensitive apps out of scope and require explicit confirmation before using shell commands or WiFi debugging. <br>
Risk: WiFi debugging can leave a device accessible beyond the intended session. <br>
Mitigation: Disconnect from the device and disable debugging when automation is finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zfinix/another) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with inline JSON and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent in using Another MCP tools; actions depend on an authorized Android device, the Another desktop app, and MCP server availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
