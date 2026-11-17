## Description:

Coordinates multiple subagents through shared STATE.yaml project files so they can track tasks, dependencies, blockers, and next actions with less central orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate project work across multiple PM-style subagents, keeping task status, dependencies, blockers, and next actions in shared project state files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes autonomous delegation to PM-style subagents with limited direct oversight.

Mitigation: Require explicit approval before spawning or messaging agents, and review delegated work before accepting it.

Risk: The skill describes persistent project state updates and git commits.

Mitigation: Keep PM state directories scoped to the intended repository and review state changes and commits before they are used as authoritative project status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/autonomous-pm)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Nicholas Carlini autonomous coding agents](https://nicholas.carlini.com/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with YAML, JavaScript, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; git is optional for persisted project-state commits.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
