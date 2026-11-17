## Description:

OpenAI Codex-native multi-agent swarm orchestration for parallel coding with git worktrees, tmux tracking, endorsement gates, native code review, integration merging, and webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkbag](https://clawhub.ai/user/linkbag)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate parallel Codex CLI agents for implementation, review, branch integration, and cleanup across git worktrees. It is intended for repositories where automated agent execution, commits, branch pushes, and optional notifications are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated agents can modify repositories, create commits, push branches, merge into main, and perform cleanup actions.

Mitigation: Run the skill first in a disposable or protected repository, keep branch protection enabled, and disable automatic main pushes unless the workflow has been reviewed.

Risk: Task IDs and task JSON influence paths, branch names, sessions, and generated runner scripts.

Mitigation: Treat task files as trusted input, review them before execution, and restrict who can supply batch task definitions.

Risk: Webhook or Telegram notifications may disclose project activity or operational details.

Mitigation: Leave external notifications disabled unless needed, and use only approved webhook URLs, bot tokens, and chat destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkbag/skills/codex-swarm)
- [Publisher profile](https://clawhub.ai/user/linkbag)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated runner scripts, git branches, commits, pull requests, logs, and notification messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository-side automation effects through Codex CLI, tmux sessions, git worktrees, review loops, merge attempts, pushes, and optional webhook or Telegram notifications.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
