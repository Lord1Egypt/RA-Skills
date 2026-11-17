## Description:

GUI automation on KylinOS V11 and V10SP1 using wlcctrl or xdotool to find, launch, focus, screenshot, click, type, drag, and verify GUI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyanogenic](https://clawhub.ai/user/cyanogenic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate GUI applications on KylinOS desktops across Wayland and X11 environments while preserving correct window-relative coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Desktop screenshots and live keyboard or mouse control can expose sensitive content or modify the wrong application.

Mitigation: Use the skill only when desktop control is acceptable, avoid passwords and private account screens, prefer window-only captures, and verify the target window before typing or clicking.

Risk: Fixed /tmp screenshot paths can leave captured desktop content in shared temporary locations.

Mitigation: Use private per-task temporary directories for screenshots and remove captured images after verification.

## Reference(s):

- [KylinOS GUI Automation Details](references/details.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash commands and bundled shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include desktop automation commands, screenshot capture paths, coordinate calculations, and verification steps.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
