## Description: <br>
Controls and interacts with real Android phones through HTTP and CLI commands for screen reading, tapping, typing, app control, calls, voice, and device I/O without ADB or root. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ier](https://clawhub.ai/user/4ier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an AI agent observe and control an authorized Android device, automate repeatable phone workflows, and capture reusable flows for future tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Android phone control can expose sensitive device actions and data. <br>
Mitigation: Install only when intentional and limit use to authorized devices, trusted target apps, and approved tasks. <br>
Risk: APK sideloading and OTA update flows can install untrusted software. <br>
Mitigation: Require explicit human approval and use only trusted APK sources before running sideload or self-update flows. <br>
Risk: SMS, contacts, location, camera, microphone, clipboard, and file operations may access or modify sensitive data. <br>
Mitigation: Require explicit approval before using these capabilities and confirm the target app, recipient, path, or data scope. <br>
Risk: Stored unlock PINs are high-value secrets. <br>
Mitigation: Avoid storing device PINs unless necessary, protect any stored PIN as a secret, and rotate it if exposed. <br>
Risk: Automating unrelated third-party app activity may violate user expectations or app rules. <br>
Mitigation: Use automation only for authorized activity and review flows before execution against third-party apps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/4ier/claw-use-android) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Android CLI commands, HTTP endpoint payloads, device setup steps, and reusable flow definitions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
