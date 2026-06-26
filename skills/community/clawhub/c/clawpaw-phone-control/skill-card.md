## Description: <br>
Guides users through ClawPaw Android setup and phone-control workflows, including APK installation, permission grants, SSH tunnel verification, ADB reconnection, MCP configuration, and stepwise device interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzliu888](https://clawhub.ai/user/wzliu888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users who intentionally connect an Android device to ClawPaw use this skill to set up ADB permissions, SSH tunneling, MCP configuration, and guided phone-control workflows. The bundled examples cover device setup, screen interaction, messaging, location-based workflows, notifications, camera capture, and other high-impact phone automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad remote control over an Android phone, including persistent credential and ADB access. <br>
Mitigation: Install only when broad phone control is intended, protect the ClawPaw secret, remove unneeded nested use-case skills, and disable wireless ADB after setup when it is no longer needed. <br>
Risk: Bundled workflows can perform high-impact actions such as messaging, posting, ride booking, attendance check-in, camera or microphone capture, location use, and notification-history review. <br>
Mitigation: Require explicit user confirmation before any message, post, ride, attendance, camera, microphone, location, or notification-history action. <br>
Risk: Setup guidance includes use of curl with TLS verification disabled and temporary screenshot files. <br>
Mitigation: Avoid curl -k where possible, verify transport security before sending secrets, and delete temporary screenshots after review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wzliu888/clawpaw-phone-control) <br>
- [ClawPaw service](https://www.clawpaw.me) <br>
- [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) <br>
- [ADBKeyboard releases](https://github.com/nicso/ADBKeyboard/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, status checks, and troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to run ADB, curl, and MCP phone-control actions after user authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
