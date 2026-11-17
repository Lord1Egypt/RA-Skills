## Description:

Safe Linux desktop automation (mouse/keyboard/screenshot) with approval mode and X11/Wayland checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pabloraka](https://clawhub.ai/user/pabloraka)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to let an agent inspect and control a Linux GUI session for browser workflows, window management, screenshots, OCR-driven state checks, and repeatable desktop tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control mouse and keyboard input, launch applications, and manipulate windows in a Linux desktop session.

Mitigation: Use a dedicated non-sensitive desktop session and keep approval mode enabled for interactive actions.

Risk: The skill can capture visible screen contents, OCR text, record video, and read or write clipboard data.

Mitigation: Treat screenshots, recordings, OCR output, and clipboard contents as sensitive data and avoid running the skill where secrets or personal data are visible.

Risk: Authoritative security evidence notes that approval mode does not cover several sensitive actions.

Mitigation: Review planned workflows before execution and restrict the agent to trusted tasks, paths, and applications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pabloraka/skills/dekstop-control-linux)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Python API calls, shell commands, and markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces desktop actions and captured files such as screenshots or recordings when invoked by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
