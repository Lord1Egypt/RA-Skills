## Description:

Maintains conversation state and project continuity across sessions by saving, restoring, and managing project contexts and progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deus-pandora](https://clawhub.ai/user/deus-pandora)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve project context across OpenClaw sessions, switch between projects, and retrieve summaries of active work, pending tasks, notes, and recent files or commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prior conversations, notes, tasks, filenames, and command text may be persisted and restored in later sessions.

Mitigation: Review saved memory before installation or use, avoid saving secrets, and provide a clear way to inspect and delete stored project and session files.

Risk: Broad automatic triggers can save or restore context when the user expected an explicit action only.

Mitigation: Prefer explicit save and restore commands, narrow automatic triggers where possible, and make memory behavior visible to the user.

Risk: Stored memory files can expose sensitive project context if filesystem permissions are too broad.

Mitigation: Restrict permissions on the memory directory and treat stored project JSON files as sensitive local data.

## Reference(s):

- [Context Engine API Reference](references/API.md)
- [ClawHub Skill Page](https://clawhub.ai/deus-pandora/skills/deus-pandora-context-engine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-formatted command results from the bundled Node.js script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists project and session state in local JSON files.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md metadata, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
