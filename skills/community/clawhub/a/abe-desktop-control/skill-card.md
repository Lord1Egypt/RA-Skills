## Description:

Advanced desktop automation with mouse, keyboard, screen capture, window management, clipboard operations, and optional autonomous task execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let an agent automate desktop workflows through mouse movement, clicking, keyboard input, screenshots, image matching, clipboard access, and window control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad desktop-control authority over mouse, keyboard, windows, clipboard, screenshots, and app-launch workflows.

Mitigation: Install only in trusted environments, keep failsafe enabled, avoid administrator execution, and review workflows before allowing them to control external accounts or sensitive applications.

Risk: Approval checks are optional and security evidence reports incomplete approval coverage.

Mitigation: Use require_approval for sensitive sessions and constrain higher-risk actions such as launching apps, submitting forms, copying clipboard content, and saving screenshots.

Risk: Screenshots and clipboard access can expose private information.

Mitigation: Do not use the skill with passwords, secrets, sensitive clipboard contents, or confidential screens, and restrict where screenshots are saved or shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/abe-desktop-control)
- [Skill documentation](artifact/SKILL.md)
- [AI agent guide](artifact/AI_AGENT_GUIDE.md)
- [Quick reference](artifact/QUICK_REFERENCE.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown documentation with Python examples; runtime calls can return text, screenshots, coordinates, window titles, and status dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Desktop actions may affect the active user session and can save screenshots or read and write clipboard text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
