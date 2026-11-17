## Description:

Structured session lifecycle for Claude Code that supports start, checkpoint, end, and daily heartbeat workflows for maintaining project state across conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to load project context, checkpoint active work, close sessions with state updates, and run daily heartbeat checks for stale items, blockers, deadlines, and memory gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow is designed to retain project context on disk, including session summaries, decisions, deadlines, blockers, and possibly sensitive notes.

Mitigation: Use it only in repositories where that local record is acceptable and review state files for sensitive content before sharing or publishing the repository.

Risk: Proposed Claude memory entries can affect future conversations for the project.

Mitigation: Review proposed memory entries before approving them and keep durable memory limited to stable, project-relevant facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conorbronsdon/skills/cot-session-management)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and state-file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local project-state updates and proposes durable memory updates for user approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
