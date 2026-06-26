## Description: <br>
Generic macOS desktop control using AppleScript for app and window semantics plus screenshot, OCR, mouse, and keyboard workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kd-oauth](https://clawhub.ai/user/kd-oauth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to perform supervised macOS desktop automation, including app activation, screenshot capture, OCR or template-based target location, mouse actions, and keyboard input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unvalidated AppleScript app names or bundle paths could trigger unintended app automation. <br>
Mitigation: Use trusted or allowlisted app names and bundle paths until AppleScript inputs are escaped or otherwise constrained. <br>
Risk: Desktop automation can capture screen content and perform clicks, drags, keyboard shortcuts, or clipboard paste actions. <br>
Mitigation: Run only in supervised sessions, grant Screen Recording and Accessibility permissions only to a trusted runtime, avoid pasting secrets, and verify targets before externally visible actions. <br>
Risk: Temporary screenshots, crops, and calibration data may remain in /tmp/macos_desktop_control after sensitive sessions. <br>
Mitigation: Clean /tmp/macos_desktop_control after sessions that involve sensitive screen content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON, text, image, or desktop-action outputs from scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write screenshots, crops, and calibration files under /tmp/macos_desktop_control.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
