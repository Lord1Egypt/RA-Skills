## Description:

Control interactive BLE devices (scan/connect/playback/timeline) from terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovappencava](https://clawhub.ai/user/lovappencava)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and device operators use this skill to scan for, connect to, and control interactive BLE devices from a terminal, including timeline playback and direct device actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a third-party npm CLI globally with the user's permissions and BLE access.

Mitigation: Use a pinned or isolated installation where practical, review the package before use, and grant BLE access only in an environment appropriate for device control.

Risk: The skill starts a background daemon that can control connected BLE devices.

Mitigation: Check daemon status during use and stop or disconnect the daemon when device control is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovappencava/skills/dokidoki)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON timeline examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include npm installation guidance and BLE device control commands.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
