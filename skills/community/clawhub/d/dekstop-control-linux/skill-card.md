## Description: <br>
Safe Linux desktop automation (mouse/keyboard/screenshot) with approval mode and X11/Wayland checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PabloRaka](https://clawhub.ai/user/PabloRaka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent automate Linux desktop interactions such as mouse and keyboard input, screenshots, screen recording, OCR, browser launching, window management, and scripted UI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control and observe the active Linux desktop, including mouse and keyboard actions, screenshots, screen recordings, OCR output, logs, and clipboard contents. <br>
Mitigation: Install it only when desktop control is intended, keep approval mode enabled, close sensitive windows, and treat captured desktop data as sensitive. <br>
Risk: Some examples disable approval mode with require_approval=False, which can allow unattended desktop actions. <br>
Mitigation: Avoid copying examples that disable approval mode unless operating in a controlled environment with no sensitive applications or credentials exposed. <br>
Risk: The skill supports workflows and login-form automation that could expose real credentials if used directly with production accounts. <br>
Mitigation: Use test accounts or injected secrets handled outside visible workflows, and do not store real credentials in presets, workflow steps, screenshots, recordings, or logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PabloRaka/dekstop-control-linux) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce desktop actions, screenshots, recordings, OCR text, logs, and clipboard-related outputs when invoked by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
