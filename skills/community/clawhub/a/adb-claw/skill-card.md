## Description: <br>
Adb Claw lets an agent observe and control a connected Android device through adb-claw and adb, including screenshots, UI interaction, deep links, app lifecycle management, monitoring, audio capture, shell commands, and file transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dionren](https://clawhub.ai/user/dionren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and automation agents use this skill to inspect and operate connected Android devices for mobile app testing, UI automation, deep-link navigation, live UI text monitoring, audio capture, and app or device lifecycle tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a connected Android device, including screenshots, UI monitoring, audio capture, shell commands, file transfer, app install or uninstall, and app data clearing. <br>
Mitigation: Require explicit user confirmation before privacy-sensitive, destructive, shell, file-transfer, app-management, or long-running monitoring actions. <br>
Risk: Connected personal devices may expose sensitive apps, accounts, screen content, UI text, or system audio to the agent. <br>
Mitigation: Use only trusted test devices where possible, avoid unattended use on devices with sensitive accounts, and disconnect or disable USB debugging when not actively using the skill. <br>
Risk: The server security verdict is suspicious because the skill's activation and consent boundaries need clearer definition for device-wide control. <br>
Mitigation: Constrain activation to explicit Android-device-control requests and confirm the user's intent before executing device-wide or privacy-sensitive commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dionren/adb-claw) <br>
- [Publisher profile](https://clawhub.ai/user/dionren) <br>
- [adb-claw project homepage](https://github.com/llm-net/adb-claw) <br>
- [adb-claw releases](https://github.com/llm-net/adb-claw/releases) <br>
- [macOS Apple Silicon adb-claw binary](https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-darwin-arm64) <br>
- [macOS Intel adb-claw binary](https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-darwin-amd64) <br>
- [Linux x86_64 adb-claw binary](https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-linux-amd64) <br>
- [Linux ARM64 adb-claw binary](https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-linux-arm64) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-oriented command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce screenshots, audio files, transferred files, or structured JSON results from the connected Android device.] <br>

## Skill Version(s): <br>
1.6.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
