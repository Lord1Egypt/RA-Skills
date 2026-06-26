## Description: <br>
Automates local desktop tasks across Windows, macOS, and Linux with mouse and keyboard control, screenshots, window handling, OCR, image recognition, clipboard access, and macro recording or playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JordaneParis](https://clawhub.ai/user/JordaneParis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agent builders use this skill when an agent needs to automate local GUI workflows that do not expose reliable APIs, including clicking, typing, reading screen text, locating images, handling windows, and replaying macros. It is intended for local workflows where the user accepts the risks of granting desktop, keyboard, mouse, clipboard, screenshot, and macro-file access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad local desktop automation powers over the screen, mouse, keyboard, clipboard, screenshots, and macro files. <br>
Mitigation: Install only when local GUI automation is required, keep safe mode enabled where practical, test actions with dry-run first, and review coordinates, window targets, and macro actions before live execution. <br>
Risk: Macro recording can capture sensitive keystrokes, private text, and window context. <br>
Mitigation: Do not record while entering credentials, payment data, private messages, tokens, or other secrets; protect saved macro files and logs as sensitive local artifacts. <br>
Risk: Replaying untrusted or unreviewed macros can execute unintended local actions. <br>
Mitigation: Avoid macros from untrusted sources, inspect macro JSON before playback, and run macros slowly or in dry-run mode before allowing real side effects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JordaneParis/desktop-automation-100per100-local) <br>
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON action results with optional generated files such as screenshots, macro JSON, CSV data, Excel files, and macro reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions may have side effects on the local desktop, keyboard, mouse, clipboard, windows, screenshots, and user-selected files; dry-run mode is documented for testing before execution.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
