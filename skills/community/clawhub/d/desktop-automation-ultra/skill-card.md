## Description:

Automates local desktop tasks across Windows, macOS, and Linux using mouse and keyboard control, screenshots, OCR, image recognition, clipboard operations, and macro recording and replay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordaneparis](https://clawhub.ai/user/jordaneparis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation users use this skill to automate repeatable desktop workflows when an application does not expose a suitable API. It is suited to local UI interaction, screen reading, window control, and macro-based task replay in environments where desktop control is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control mouse and keyboard input, interact with windows, use the clipboard, and capture the screen in the active desktop session.

Mitigation: Use it only in a dedicated profile or non-sensitive environment, keep safe mode enabled, and test actions with dry-run before allowing real desktop changes.

Risk: Macro recording can capture sensitive keystrokes, window titles, screenshots, logs, and other local workflow data.

Mitigation: Do not record while entering passwords, payment data, private messages, or tokens; store generated macros, logs, screenshots, and reports as sensitive files.

Risk: Macro replay can execute a sequence of clicks, keystrokes, clipboard actions, and screen-driven operations from a file.

Mitigation: Play only trusted macros, inspect macro JSON before use, run macros in dry-run or at reduced speed first, and avoid macros from untrusted sources.

Risk: OCR, screenshots, clipboard operations, and report generation can expose data visible on screen or copied locally.

Mitigation: Limit use to workflows where screen and clipboard contents are appropriate to process, and clean up or protect generated output files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jordaneparis/skills/desktop-automation-ultra)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [JSON action results, Markdown or text guidance, shell commands, configuration snippets, saved screenshots, macro JSON files, and optional HTML/JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local logs, screenshots, recorded macros, encrypted macro files, clipboard contents, and execution reports depending on the requested action.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
