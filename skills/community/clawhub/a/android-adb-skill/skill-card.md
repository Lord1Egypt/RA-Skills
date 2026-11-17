## Description:

Android Adb Skill guides agents through Android debugging workflows with ADB, including device detection, APK installation, log capture, app and device inspection, file transfer, screenshots, wireless ADB setup, and reboot commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhongm](https://clawhub.ai/user/yhongm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate connected Android devices through ADB during debugging, testing, app installation, log review, and verification of Android-related code changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ADB commands can change device state or erase app data.

Mitigation: Require explicit user approval before installs, uninstalls, data clearing, reboots, file writes, and wireless ADB changes.

Risk: User-provided package names, serials, and paths can cause unintended commands against the wrong app, file, or device.

Mitigation: Run device detection first, require target-device selection when multiple devices are connected, and confirm commands containing user-provided paths or package names before execution.

## Reference(s):

- [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should show executed commands, preserve command output in code blocks, explain failures, and guide multi-device selection when needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
