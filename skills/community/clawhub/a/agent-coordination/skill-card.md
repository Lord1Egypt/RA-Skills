## Description:

Coordinates autonomous coding-agent teams with Chief of Staff workflows, task delegation patterns, VibeKanban task management, and CI monitoring guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianrwagner](https://clawhub.ai/user/brianrwagner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, DevOps engineers, and product managers use this skill to break complex coding work into scoped tasks, delegate execution to autonomous agents, track status through VibeKanban, and monitor pull request CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Chief of Staff mode can turn later user requests into task delegation until the mode is explicitly exited.

Mitigation: Confirm when CoS mode is active and explicitly exit the mode when coordination is complete.

Risk: The skill can create VibeKanban tasks and start coding-agent workspace sessions.

Mitigation: Confirm the project, repository, branch, executor, and task scope before launching agent sessions.

Risk: CI monitoring may inspect pull request check status and failed logs through the GitHub CLI.

Mitigation: Confirm the target pull request and repository before inspecting CI logs.

Risk: The artifact includes a hard-coded local repository exception in its coordination behavior.

Mitigation: Do not rely on that local exception outside its original environment; require explicit user confirmation before any direct execution.

## Reference(s):

- [Agent Coordination on ClawHub](https://clawhub.ai/brianrwagner/skills/agent-coordination)
- [Task Templates](examples/task-templates.md)
- [Chief of Staff Workflow](references/cos-workflow.md)
- [Delegation Patterns](references/delegation-patterns.md)
- [VibeKanban MCP API Reference](references/vibekanban-api.md)
- [GitHub CLI](https://cli.github.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with task templates, status tables, MCP tool calls, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include VibeKanban task descriptions, task status summaries, delegation plans, escalation notes, and CI monitoring commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
