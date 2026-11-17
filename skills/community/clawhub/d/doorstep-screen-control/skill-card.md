## Description:

Enables an agent to use OpenClaw Node and local Python tools to capture screenshots, locate text or images, and control mouse and keyboard actions on a desktop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncsimok](https://clawhub.ai/user/ncsimok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent needs controlled desktop automation for non-browser applications, file workflows, or visual UI tasks that require screenshots, OCR, image matching, mouse actions, and keyboard input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent view the screen and control mouse and keyboard input.

Mitigation: Use it only on systems where this access is intentional, review screenshots before actions, and require user confirmation for destructive or sensitive workflows.

Risk: Persistent node installation and local script execution can broaden access on sensitive systems.

Mitigation: Prefer the foreground loopback node run mode, avoid administrator service installation unless operationally required, and confirm how to stop the node, revoke pairings, and restrict local exec.

## Reference(s):

- [Screen Control Node setup guide](references/setup-guide.md)
- [Tesseract OCR installation guide](https://github.com/UB-Mannheim/tesseract/wiki)
- [ClawHub skill page](https://clawhub.ai/ncsimok/skills/doorstep-screen-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots or local screenshot file paths when the screen control script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
