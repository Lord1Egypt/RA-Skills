## Description:

Maintains conversation state and project continuity across OpenClaw sessions by tracking active projects, saving and restoring context, and supporting project management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deus-pandora](https://clawhub.ai/user/deus-pandora)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve project context across sessions, restore the last active project, track pending tasks and notes, and switch between active projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved project context may include sensitive notes, filenames, commands, tasks, or other confidential session details.

Mitigation: Avoid saving secrets or confidential notes, periodically review the persisted JSON files, and clear records that are no longer needed.

Risk: The skill persists memory in local JSON files, so context can remain available across future sessions on the same environment.

Mitigation: Use the skill only when persistent project context is desired and tighten local filesystem permissions where appropriate.

## Reference(s):

- [Context Engine skill page](https://clawhub.ai/deus-pandora/skills/deus-context-engine)
- [Context Engine API Reference](references/API.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON-backed project context records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists project and session context in local JSON files under the documented memory directory.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter and changelog report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
