## Description:

Full desktop automation - screenshots, mouse, keyboard, window management, clipboard, screen info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qoohsuan](https://clawhub.ai/user/qoohsuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent inspect and control a local desktop GUI through screenshots, mouse actions, keyboard input, window management, clipboard access, screen queries, and timed waits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Desktop automation can expose sensitive information through screenshots, active windows, typed text, or clipboard reads.

Mitigation: Close or hide sensitive windows before use, avoid storing secrets in the clipboard, and prefer region screenshots when full-screen capture is not needed.

Risk: Keyboard shortcuts and typing may affect the wrong application if the active window is not the intended target.

Mitigation: Verify or activate the target window before sending text, hotkeys, close commands, or other destructive actions.

Risk: Mouse and keyboard automation can continue until interrupted if a command behaves unexpectedly.

Mitigation: Keep pyautogui failsafe enabled and avoid the --no-failsafe option unless there is a deliberate operational reason.

Risk: Setup installs Python packages at runtime, so dependency changes can affect behavior over time.

Mitigation: Pin and review dependencies before running setup in controlled or production environments.

## Reference(s):

- [Atu Desktop Control on ClawHub](https://clawhub.ai/qoohsuan/skills/atu-desktop-control)
- [qoohsuan Publisher Profile](https://clawhub.ai/user/qoohsuan)
- [OpenClaw](https://github.com/nichochar/openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON command results and local screenshot files, with Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands report ok/error status for agent parsing; screenshots are saved locally.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill frontmatter, script version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
