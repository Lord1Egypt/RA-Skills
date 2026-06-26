## Description: <br>
Desktop Gui helps agents automate desktop GUI workflows with Python, xdotool, scrot, OCR, and optional vision-model screen analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baimaxx](https://clawhub.ai/user/baimaxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users can use this skill to generate Python and shell-command guidance for controlling local desktop applications, taking screenshots, recognizing UI elements, and managing windows when no API is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to move the mouse, type, click, take screenshots, and manage real desktop windows. <br>
Mitigation: Use a VM or disposable desktop session, close sensitive windows, keep failsafe and pause controls enabled, and require manual approval before clicks or typing. <br>
Risk: The recommended vision workflow can upload full-screen screenshots to a hard-coded HTTP model endpoint. <br>
Mitigation: Prefer local OCR or a local vision model; if a remote endpoint is intentional, use a controlled HTTPS endpoint and crop or redact screenshots before sending them. <br>
Risk: The visual model example uses a bearer token for model access. <br>
Mitigation: Store credentials outside scripts, avoid exposing them in shell history or logs, and rotate the token if it may have been shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baimaxx/desktop-gui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and bash code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include desktop automation steps, dependency installation commands, screenshots or OCR workflow guidance, and safety precautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
