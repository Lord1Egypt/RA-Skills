## Description:

Smart Context Engine maintains conversation state and project continuity across OpenClaw sessions by tracking active projects, saving and restoring context, and supporting project management commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deus-pandora](https://clawhub.ai/user/deus-pandora)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to preserve project continuity across sessions, restore the last active project, manage pending tasks, and summarize current progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically persists project context, notes, file paths, command metadata, and task history in plaintext under the OpenClaw memory directory.

Mitigation: Install only where local filesystem permissions are acceptable, avoid saving secrets or sensitive commands, and review stored project memory regularly.

Risk: The scanner verdict is suspicious because the skill lacks clear opt-in, deletion, and permission-hardening controls for persisted session data.

Mitigation: Use the skill in environments where persistent memory is expected and add operational controls for consent, deletion, and access restrictions before broader deployment.

## Reference(s):

- [Context Engine API Reference](artifact/references/API.md)
- [ClawHub Skill Page](https://clawhub.ai/deus-pandora/skills/context-engine-deus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON command results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local project state summaries, task updates, context restoration messages, and command-line usage guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and changelog, released 2026-02-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
