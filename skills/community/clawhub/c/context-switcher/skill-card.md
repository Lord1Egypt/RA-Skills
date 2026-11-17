## Description:

Switches OpenClaw between life modes (Work/Focus, Personal, Creative, Do Not Disturb). Triggered by natural language or calendar events. Each mode reshapes notification filtering, memory surface, response style, and auto-restores when the session ends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taha2053](https://clawhub.ai/user/taha2053)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to switch an OpenClaw assistant between work, personal, creative, and do-not-disturb modes. It adjusts notification handling, mode profile context, response style, session summaries, and restore behavior for the active mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic mode changes can affect notifications and local assistant context without an explicit command.

Mitigation: Disable auto-triggering unless calendar and phrase-based activation are desired, and require explicit user confirmation for sensitive contexts.

Risk: Do Not Disturb behavior may silently log incoming messages for later review.

Mitigation: Use DND logging only when needed, disclose where logs are stored, and clear logs after restore.

Risk: Server security evidence reports a path handling issue that can read or write outside the intended context-switcher directory.

Mitigation: Review and fix package layout and path handling before installation so state, profile, and snapshot files remain inside the skill directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taha2053/skills/context-switcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command outputs and JSON-backed local state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads editable mode profiles and writes local context or snapshot state during mode switching and restore.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
