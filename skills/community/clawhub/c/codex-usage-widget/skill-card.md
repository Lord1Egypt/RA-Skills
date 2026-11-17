## Description:

Install, update, inspect, or uninstall a local-only Übersicht desktop widget that tracks Codex token usage, recent root sessions, source labels, and context-window pressure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex users use this skill to install, update, inspect, or remove a local macOS Übersicht widget for monitoring Codex usage and recent root-session activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The widget repeatedly reads local Codex usage metadata and thread titles from ~/.codex.

Mitigation: Install it only on trusted local desktops where displaying Codex usage and session metadata is acceptable.

Risk: Install and uninstall scripts replace or remove the fixed Übersicht widget folder for this widget.

Mitigation: Review the destination path before running install or uninstall commands, especially on systems with customized Übersicht widget layouts.

Risk: The widget depends on Codex local storage fields that may change across Codex releases.

Mitigation: Validate after installation by running the documented Python command and checking for JSON with ok set to true.

## Reference(s):

- [Übersicht](https://tracesof.net/uebersicht/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local installation, update, validation, and uninstall guidance for an Übersicht widget.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
