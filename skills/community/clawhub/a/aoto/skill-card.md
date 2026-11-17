## Description:

Desktop automation via native OS accessibility trees using the agent-desktop CLI for observing, interacting with, and automating desktop applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darryek](https://clawhub.ai/user/darryek)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to guide AI agents through desktop GUI automation tasks such as reading UI state, clicking controls, filling forms, handling windows, using the clipboard, and working with notifications. The documented workflow is macOS-focused and depends on the external agent-desktop CLI plus Accessibility permission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad desktop observation and control through macOS Accessibility permissions.

Mitigation: Use it only in a trusted desktop session, require explicit user approval before controlling sensitive apps or windows, and revoke Accessibility permission when finished.

Risk: The documented install path uses an external CLI and includes an unpinned Bun trusted-install option.

Mitigation: Prefer a pinned and verified CLI version, and avoid the Bun trusted install path unless the package has been audited.

Risk: Automation commands can expose screenshots, clipboard contents, notifications, and sensitive UI state.

Mitigation: Do not allow agents to read or act on screenshots, clipboard contents, notifications, or sensitive app windows without explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darryek/skills/aoto)
- [Observation Commands](references/commands-observation.md)
- [Interaction Commands](references/commands-interaction.md)
- [System Commands](references/commands-system.md)
- [Common Automation Workflows](references/workflows.md)
- [macOS Platform](references/macos.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with shell command examples and JSON output contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of an external CLI that returns JSON envelopes and may produce screenshots or clipboard-derived text when invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
