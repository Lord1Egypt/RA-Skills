## Description:

Agent Memento is a tick-driven framework for long-running LLM coding agents that uses cron-style workers, Markdown planning files, verification commands, and an optional dashboard to manage autonomous project execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangwenyu2](https://clawhub.ai/user/yangwenyu2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to scaffold and operate a local autonomous coding workflow where short-lived agents execute tasks from Markdown plans, run verification commands, update status files, and report progress through a dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous background workers can repeatedly modify project files and run verification commands.

Mitigation: Install and run the skill only in an isolated VM, container, or disposable worktree, and treat every MASTER_PLAN verify command as executable code requiring review.

Risk: Rollback and cleanup behavior can affect valuable uncommitted or untracked files.

Mitigation: Do not initialize Agent Memento inside an existing repository with important uncommitted changes or private files.

Risk: Dashboard controls and preview features can expose local project contents if served beyond localhost.

Mitigation: Keep the dashboard bound to localhost unless authentication and network controls are added, and do not use preview mode with secrets in the project tree.

Risk: Dashboard dependencies may contain outdated or vulnerable packages.

Mitigation: Update and audit the dashboard dependencies before relying on the dashboard in a persistent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangwenyu2/skills/agent-memento)
- [Publisher profile](https://clawhub.ai/user/yangwenyu2)
- [Artifact README](artifact/README.md)
- [Artifact skill specification](artifact/SKILL.md)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated project scaffolding]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local project state files, tick-worker shell scripts, dashboard assets, and operational instructions.]

## Skill Version(s):

2.0.15 (source: server release metadata and artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
