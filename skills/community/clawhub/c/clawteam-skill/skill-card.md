## Description:

Multi-agent swarm coordination via the ClawTeam CLI for creating teams, spawning parallel agents, coordinating dependent tasks, messaging agents, monitoring kanban progress, and launching templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xybio](https://clawhub.ai/user/xybio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and operate ClawTeam-based multi-agent workflows for complex software, code review, research, or analysis tasks. It helps agents provide setup, task orchestration, monitoring, messaging, safety checkpoints, and cleanup guidance for ClawTeam teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external clawteam CLI and spawned agents can perform high-impact actions in a repository.

Mitigation: Verify and pin the CLI before use, run it only in trusted repositories, and keep permission prompts enabled.

Risk: Subprocess spawns, branch merges, forced cleanup, and web dashboard exposure can change code or expose local workflow state.

Mitigation: Require explicit review before approving these operations and use bounded monitoring instead of unattended loops.

Risk: Secrets shared through tasks, worktrees, or agent messages may be exposed to spawned agents or persisted in local state.

Mitigation: Do not place bot tokens, app secrets, webhook secrets, or other credentials in team tasks, worktrees, or chat messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xybio/skills/clawteam-skill)
- [ClawTeam upstream project](https://github.com/win4r/ClawTeam-OpenClaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is instruction-only and expects the external clawteam CLI to be installed separately.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
