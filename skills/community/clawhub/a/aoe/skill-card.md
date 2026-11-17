## Description:

Manage AI coding agent sessions via Agent of Empires (aoe)

This skill is ready for commercial/non-commercial use.

## Publisher:

[njbrake](https://clawhub.ai/user/njbrake)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create, organize, monitor, and manage AI coding agent sessions in tmux, including sessions based on Git worktrees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session commands can start or stop agents, send prompts, and remove sessions; purge options can permanently delete worktrees and branches.

Mitigation: Check the session and worktree targets before acting, review prompts before sending them, and use purge or delete options only when permanent removal is intended.

## Reference(s):

- [Agent of Empires project](https://github.com/agent-of-empires/agent-of-empires)
- [Sandbox guide](https://github.com/agent-of-empires/agent-of-empires/blob/main/docs/guides/sandbox.md)
- [Agent of Empires on ClawHub](https://clawhub.ai/njbrake/skills/aoe)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover session management, status inspection, and configuration.]

## Skill Version(s):

1.24.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
