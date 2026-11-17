## Description:

Persistent local memory system for AI agents that stores user preferences, project context, and feedback as local Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siyu-hu](https://clawhub.ai/user/siyu-hu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve local cross-session notes about preferences, project context, behavioral feedback, and reference links. It helps an agent resume work by reading a memory index and writing concise Markdown memory files when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memories can have too much automatic influence over future agent behavior.

Mitigation: Treat memories as context rather than instructions, and do not let them override higher-priority safety or session instructions.

Risk: Local cross-session notes may retain sensitive user or project context if written too broadly.

Mitigation: Constrain memory to a specific user or project directory, require confirmation before writes, and review stored feedback regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siyu-hu/skills/agent-local-memory)
- [ClawHub publisher profile](https://clawhub.ai/user/siyu-hu)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown memory files, MEMORY.md index entries, and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local file storage paths for Claude Code, OpenClaw, or a cross-platform agent memory directory.]

## Skill Version(s):

1.0.1 (source: server release metadata; SKILL.md frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
