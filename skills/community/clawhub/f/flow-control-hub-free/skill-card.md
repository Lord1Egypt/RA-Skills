## Description: <br>
Flow Control Hub Free guides agents through local desktop automation tasks such as mouse control, keyboard input, screenshots, and basic RPA workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, and operations users use this skill to create local desktop automation workflows for mouse actions, keyboard input, screenshot capture, form filling, QA evidence capture, and multi-window data transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated clicks and keystrokes can act on the wrong live window, submit unintended input, or save files without enough safeguards. <br>
Mitigation: Use the skill only in controlled desktop sessions, keep unrelated or sensitive windows closed, enable fail-safe interruption and operation pauses, and inspect generated scripts before they click, type, press Enter, or save files. <br>
Risk: Screenshots and logs can capture credentials or other sensitive information. <br>
Mitigation: Avoid login, financial, and account-management screens; treat saved screenshots and logs as sensitive files; and redact or delete captures that include secrets. <br>


## Reference(s): <br>
- [Flow Control Hub Free on ClawHub](https://clawhub.ai/thcjp/skills/flow-control-hub-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local desktop automation examples that can click, type, save files, and capture screenshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
