## Description: <br>
Automates local desktop tasks on Windows, macOS, and Linux with mouse and keyboard control, screenshots, OCR, image recognition, macro recording, and macro replay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JordaneParis](https://clawhub.ai/user/JordaneParis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and power users use this skill to automate local desktop workflows when an application does not expose an API. It is suited for reviewed, non-sensitive GUI tasks that need screenshots, OCR, image matching, clipboard actions, or repeatable macros. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control the local desktop, including mouse clicks, keyboard input, clipboard operations, and macro replay. <br>
Mitigation: Keep safe mode enabled, test workflows with dry_run first, and run only macros that were created or reviewed by the user. <br>
Risk: Screen reading, OCR, screenshots, and keyboard recording can expose passwords, private messages, payment data, or other sensitive information. <br>
Mitigation: Use the skill only for non-sensitive workflows and keep credentials and private screens out of view while recording, OCR, or screenshots are active. <br>
Risk: Saved macros, screenshots, logs, and reports can retain sensitive workflow details after execution. <br>
Mitigation: Treat generated files as sensitive, store them in restricted locations, and review them before sharing or replaying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JordaneParis/desktop-automation-ultra) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact license](artifact/LICENSE.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON action results, and local file outputs such as screenshots, macros, logs, and reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create sensitive local artifacts, including recorded macros, screenshots, OCR output, audit logs, and execution reports.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
