## Description: <br>
Advanced desktop automation with mouse, keyboard, and screen control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to control desktop applications through mouse, keyboard, screen capture, image matching, window management, and clipboard operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control the full desktop, including mouse input, keyboard input, windows, clipboard contents, and screenshots. <br>
Mitigation: Use it only in a clean or separate desktop session, keep sensitive windows and clipboard contents clear, and avoid unattended autonomous runs. <br>
Risk: Safety controls are incomplete and can be disabled for speed. <br>
Mitigation: Leave failsafe enabled, prefer approval mode for sensitive actions, and review planned actions before execution. <br>
Risk: Screenshots and optional LLM/API integrations can expose sensitive desktop data. <br>
Mitigation: Treat screenshots, saved image files, API prompts, and API responses as sensitive data flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quincygunter/abe-desktop-control) <br>
- [Desktop Control Skill](artifact/SKILL.md) <br>
- [AI Desktop Agent - Cognitive Automation Guide](artifact/AI_AGENT_GUIDE.md) <br>
- [Desktop Control - Quick Reference Card](artifact/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown documentation with Python and bash code blocks; runtime calls may return Python objects, result dictionaries, screenshots, and saved image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automation can affect the active desktop, clipboard, open windows, and saved screenshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
