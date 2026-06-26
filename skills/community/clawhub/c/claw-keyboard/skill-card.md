## Description: <br>
Claw Keyboard helps agents discover and control compatible USB HID keyboards, including RGB lighting, custom LEDs, macros, key mapping, profile settings, KLE layout rendering, and multi-keyboard management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dionren](https://clawhub.ai/user/dionren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent inspect and operate compatible USB HID keyboards, adjust lighting and profiles, manage macros and keymaps, and produce layout output when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required third-party binary can control connected keyboard hardware. <br>
Mitigation: Install only when the binary source is trusted and verify release checksums when possible. <br>
Risk: Reset, macro, keymap, and flash-save commands can make lasting hardware changes or erase keyboard settings. <br>
Mitigation: Run those commands only after explicit user approval and confirm the intended change before execution. <br>
Risk: When multiple compatible keyboards are connected, commands may affect the wrong device. <br>
Mitigation: Run discovery first and use the device selector for the intended keyboard. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dionren/claw-keyboard) <br>
- [Claw Keyboard GitHub Repository](https://github.com/clawdevice/claw-keyboard) <br>
- [macOS Apple Silicon Binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-darwin-arm64) <br>
- [macOS Intel Binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-darwin-amd64) <br>
- [Linux x86_64 Binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-linux-amd64) <br>
- [Linux ARM64 Binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-linux-arm64) <br>
- [Windows x86_64 Binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-windows-amd64.exe) <br>
- [Windows ARM64 Binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-windows-arm64.exe) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Files] <br>
**Output Format:** [Markdown or plain text with shell commands, command-output summaries, and optional JSON or SVG outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use the claw-keyboard --json flag for machine-readable output and KLE rendering commands for SVG files.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
