## Description: <br>
Guides agents through Android development debugging with ADB, including device detection, APK installation, logcat capture, app management, file transfer, device information checks, wireless ADB, and reboot commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhongm](https://clawhub.ai/user/yhongm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate Android devices through ADB while validating Android, Flutter, or HarmonyOS code changes, collecting logs, installing builds, and troubleshooting connected-device workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over connected Android devices through ADB, including disruptive actions such as uninstalling apps, clearing app data, force-stopping apps, rebooting devices, and running shell commands. <br>
Mitigation: Confirm the exact connected device and package name before use, and require manual confirmation before uninstalling apps, clearing app data, force-stopping apps, rebooting, or running shell commands. <br>
Risk: ADB actions can affect the wrong target when multiple devices or package names are present. <br>
Mitigation: Run device detection before each ADB operation and require the user to select a target device when more than one device is connected. <br>


## Reference(s): <br>
- [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command-output code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows the ADB commands to run, preserves command output in code blocks, and explains results and failures in Chinese.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
