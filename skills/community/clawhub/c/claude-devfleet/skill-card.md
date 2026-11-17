## Description:

Orchestrates multi-agent coding work through Claude DevFleet by planning projects, dispatching parallel agents in isolated worktrees, monitoring progress, and reading structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gensandee-na](https://clawhub.ai/user/gensandee-na)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multiple Claude Code agents on coding projects, review generated mission plans, dispatch work, monitor progress, and summarize completed changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic dispatch and merge behavior can apply agent-generated code changes before a team has reviewed them.

Mitigation: Review the generated mission plan before dispatch and use protected branches or manual review settings when automatic merges are not desired.

Risk: The skill depends on a local DevFleet service that can coordinate multiple coding agents.

Mitigation: Install and use it only when that coordination behavior is intended for the current workspace.

## Reference(s):

- [Claude Devfleet on ClawHub](https://clawhub.ai/gensandee-na/skills/claude-devfleet)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and structured progress summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates a local Claude DevFleet service through MCP when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
