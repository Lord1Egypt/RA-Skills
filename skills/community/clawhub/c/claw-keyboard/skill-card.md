## Description:

Controls keyboard RGB backlight, custom LEDs, macros, key mapping, and profile settings via USB HID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dionren](https://clawhub.ai/user/dionren)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover and control compatible USB HID keyboards, including lighting, macros, key mappings, profiles, and KLE layout rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Native binaries are downloaded from a mutable latest-release channel without pinned verification.

Mitigation: Install only from a trusted publisher and prefer a version-pinned release with digest verification enforced before execution.

Risk: The suggested Linux hidraw udev rule grants broad persistent device permissions.

Mitigation: Narrow the rule to the specific keyboard interface or use a dedicated group or active-session access mechanism.

Risk: Some commands can change key bindings, erase macros, reset the keyboard, or persist settings to flash.

Mitigation: Require explicit user confirmation before running state-changing commands, and prefer read-only commands for discovery and inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dionren/skills/claw-keyboard)
- [Project homepage](https://github.com/clawdevice/claw-keyboard)
- [macOS Apple Silicon binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-darwin-arm64)
- [macOS Intel binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-darwin-amd64)
- [Linux x86_64 binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-linux-amd64)
- [Linux ARM64 binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-linux-arm64)
- [Windows x86_64 binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-windows-amd64.exe)
- [Windows ARM64 binary](https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-windows-arm64.exe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI actions may produce text, JSON, or SVG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Machine-readable CLI output is available with --json; commands that change hardware state require explicit user confirmation.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
