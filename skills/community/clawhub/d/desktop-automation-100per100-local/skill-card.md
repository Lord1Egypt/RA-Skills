## Description:

Automate local desktop tasks with mouse, keyboard, window control, OCR, image recognition, screenshots, clipboard access, and macro recording or playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordaneparis](https://clawhub.ai/user/jordaneparis)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation users use this skill to let an agent operate local desktop applications where no API is available, including clicking, typing, reading screen text, recognizing UI images, managing windows, and replaying macros. It is suited to intentionally authorized local workflows that can tolerate desktop-control risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control the local desktop, including mouse, keyboard, windows, clipboard, and screen capture.

Mitigation: Install only for intentional local automation, run under a least-privileged account, and avoid sensitive applications or admin prompts.

Risk: Macro recording can capture keystrokes, window titles, screenshots, clipboard data, private messages, credentials, or payment information.

Mitigation: Do not record sensitive workflows, inspect macro JSON before playback, and store macros, screenshots, reports, and logs in protected locations.

Risk: Safety controls are incomplete and desktop actions may still cause unintended side effects.

Mitigation: Keep safe mode enabled, test actions with dry-run first, review generated macros before replay, and prefer pinned dependencies in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jordaneparis/skills/desktop-automation-100per100-local)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Dependencies](artifact/DEPENDENCIES.md)
- [License](artifact/LICENSE.txt)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration]

**Output Format:** [JSON action results, extracted text, generated local files, and setup or execution commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create screenshots, macro JSON, audit logs, clipboard content, and HTML or JSON reports depending on the requested action.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
