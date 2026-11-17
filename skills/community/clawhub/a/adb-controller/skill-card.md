## Description:

Controls an Android device via ADB for taps, swipes, text input, and other commands, then captures a screenshot of the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengyang0317](https://clawhub.ai/user/fengyang0317)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to control a connected Android device through ADB commands and inspect the resulting device state through screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill permits broad ADB control over the target Android device.

Mitigation: Install and use it only for devices where agent-driven ADB actions are acceptable, and review intended commands before execution.

Risk: The selected ADB target can be driven by environment configuration.

Mitigation: Verify the device or server address before use and avoid untrusted ADB_SERVER_ADDRESS values.

Risk: Screenshots saved after commands may contain sensitive screen contents.

Mitigation: Treat saved screenshots as sensitive files and delete them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengyang0317/skills/adb-controller)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and screenshot file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captures a PNG screenshot after each ADB command.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
