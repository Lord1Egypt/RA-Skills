## Description:

Coordinates multi-agent coding, writing, analysis, and image workflows through tmux-driven Claude Code and Codex sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayao99315](https://clawhub.ai/user/ayao99315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering leads use this skill to decompose software work into agent tasks, dispatch Claude Code or Codex sessions, monitor progress, coordinate reviews, and report completion across a local swarm workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe default privileges can let delegated agents run high-impact commands without normal approval or sandbox prompts.

Mitigation: Review generated prompts before dispatch and remove bypass permission flags unless the workflow runs in an isolated, disposable repository.

Risk: Automatic Git push and force-commit behavior can publish unintended changes or sensitive files.

Mitigation: Use repositories without secrets, inspect changed files before commit or push, and narrow or disable auto-push and force-commit defaults.

Risk: Persistent post-commit hooks can affect future repository work after the swarm workflow ends.

Mitigation: Inspect or back up existing Git hooks before installation and uninstall the swarm hook after the workflow is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayao99315/skills/ayao-workflow-agent)
- [Agent Swarm Playbook](references/agent-swarm-playbook.md)
- [Task Schema](references/task-schema.md)
- [Architecture Review](docs/arch-review-2026-03-22.md)
- [Fix Review](docs/review-fix-2026-03-22.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command blocks and JSON task schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local swarm state updates, agent dispatch commands, review routing, and hook-based workflow coordination.]

## Skill Version(s):

1.7.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
