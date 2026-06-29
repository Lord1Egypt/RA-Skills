## Description: <br>
Gives AI agents a camera-guided robot arm interface for tapping, swiping, OCR, screenshots, and YAML automation on real smartphones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hamlet0168](https://clawhub.ai/user/hamlet0168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and automation engineers use this skill to let an agent control a real phone through a local FlexArm robot-arm service, including physical taps, swipes, OCR-based lookup, screenshots, and scripted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated taps, swipes, and scripts operate a real phone and can take unintended actions in apps or accounts. <br>
Mitigation: Use dedicated or low-risk devices and accounts where possible, define task boundaries before execution, and monitor or stop scripts when behavior diverges from the intended workflow. <br>
Risk: OCR, screenshots, and saved logs may expose sensitive on-screen information. <br>
Mitigation: Use the skill only on phones and accounts where screen capture and OCR are acceptable, and avoid displaying secrets, private messages, or regulated data during automation. <br>
Risk: The local hardware-control service and configuration changes can affect the robot arm, camera, gesture settings, and scheduled automation. <br>
Mitigation: Install FlexArm software only from trusted sources, verify service health before actions, and limit agent permission to run scripts or change daily, app, and gesture configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hamlet0168/flexarm-robot-arm) <br>
- [FlexArm release page](https://github.com/hamlet0168/flexarm/releases) <br>
- [FlexArm v2.0.1 release](https://github.com/hamlet0168/flexarm/releases/tag/v2.0.1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON API payloads, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance targets a local HTTP hardware-control service on port 7826 and may include scripts or configuration for phone automation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
