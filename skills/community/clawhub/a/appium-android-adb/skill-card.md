## Description: <br>
Read and control any Android app via Appium or uiautomator2, using a persistent bridge daemon with dump, tap, scroll, type, wait, screenshot, and direct uiautomator2 workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlittlebear](https://clawhub.ai/user/openlittlebear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect Android app screens and issue controlled Appium, uiautomator2, or ADB actions against a connected Android device. It is especially aimed at native Android views and UC WebView-based apps where structured dumps, coordinate taps, screenshots, and backend-specific scrolling guidance are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently read and control a connected Android device. <br>
Mitigation: Use it only with devices and apps you intend to automate, and stop the bridge when the task is complete. <br>
Risk: Local IPC files and screenshots under /tmp may expose device state on shared or multi-user machines. <br>
Mitigation: Run on a trusted single-user workstation, clear temporary bridge files and screenshots after use, and avoid sensitive screens. <br>
Risk: The Appium startup path uses insecure and relaxed security flags. <br>
Mitigation: Review the Appium flags before running, restrict access to localhost, and avoid using the bridge around banking, messaging, password, payment, or account-recovery workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlittlebear/appium-android-adb) <br>
- [Publisher profile](https://clawhub.ai/user/openlittlebear) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime bridge commands return JSON responses for screen dumps, element matches, taps, scrolls, screenshots, typing, and waits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
