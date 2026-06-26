## Description: <br>
Executes Android Debug Bridge commands for connected-device management, app management, debugging, screen capture, performance checks, file transfer, input simulation, network control, and system inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cwener](https://clawhub.ai/user/cwener) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and Android support teams use this skill to translate natural-language Android debugging or device-management requests into ADB workflows and shell commands. It helps inspect connected devices, capture logs and screenshots, manage apps, transfer files, profile performance, and apply explicit confirmation gates for destructive operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ADB-level access can inspect, modify, reboot, wipe, or otherwise control connected Android devices. <br>
Mitigation: Require users to review exact commands before sensitive actions and require explicit confirmation for destructive operations such as app-data clearing, uninstall, reboot, wipe, flashing, root, or system-setting changes. <br>
Risk: Log, screenshot, recording, UI-dump, and file-transfer commands can expose private app or device data. <br>
Mitigation: Treat captured artifacts as sensitive, write them only to user-approved paths, and avoid sharing or persisting device data unless the user explicitly requests it. <br>
Risk: The security evidence flags unsafe shell command construction around log capture and warns against untrusted logcat tags, serials, package names, or paths. <br>
Mitigation: Review and constrain serials, package names, tags, and file paths before invoking helper scripts, and avoid untrusted values until the log-capture helper is fixed. <br>


## Reference(s): <br>
- [ADB Command Reference](references/adb-commands.md) <br>
- [ClawHub Release Page](https://clawhub.ai/cwener/android-adb-2) <br>
- [Android Platform Tools for Linux](https://dl.google.com/android/repository/platform-tools-latest-linux.zip) <br>
- [Android Platform Tools for macOS](https://dl.google.com/android/repository/platform-tools-latest-darwin.zip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and command-output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute ADB commands against connected Android devices; long-running log output may be routed to a separate terminal or an explicit output file.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
