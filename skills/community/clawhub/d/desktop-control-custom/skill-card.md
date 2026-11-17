## Description:

Advanced desktop automation with mouse, keyboard, screen, window, clipboard, and task-level control for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbingquanxu-cpu](https://clawhub.ai/user/alexbingquanxu-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to let an agent inspect the desktop, move the mouse, type, trigger hotkeys, manage windows, use the clipboard, capture screenshots, and execute simple autonomous desktop tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants an agent live control over the mouse, keyboard, windows, screen capture, and clipboard.

Mitigation: Install only in a controlled environment, keep failsafe enabled, avoid administrator execution unless required, and use approval mode or code review before autonomous workflows.

Risk: Screenshots, window titles, and clipboard reads can expose sensitive information from the active desktop session.

Mitigation: Run the skill away from sensitive screens and clipboard contents, and clear or isolate sensitive data before allowing screen or clipboard operations.

Risk: Autonomous desktop tasks can interact with the wrong application or perform unintended clicks, typing, hotkeys, or file operations.

Mitigation: Use explicit task scopes, verify the active window before execution, set reasonable step limits, and review action logs or captured screenshots after runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexbingquanxu-cpu/skills/desktop-control-custom)
- [Publisher profile](https://clawhub.ai/user/alexbingquanxu-cpu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Python snippets, shell commands, and runtime action results such as screenshots, window titles, clipboard text, and status dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce desktop side effects through mouse, keyboard, clipboard, screenshots, and window focus changes.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
