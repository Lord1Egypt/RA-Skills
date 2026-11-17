## Description:

Fast Claude Code runs Claude Code tasks in background tmux sessions with Single, Interactive, and Team modes, then notifies the user through a completion callback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadlining](https://clawhub.ai/user/deadlining)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to launch Claude Code work in the background, keep long-running or multi-agent sessions alive, and receive completion notifications without polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto mode runs Claude Code with broad unattended authority.

Mitigation: Use plan mode by default and enable auto mode only in trusted, version-controlled projects after reviewing the task and scripts.

Risk: Callbacks can forward task text and output through OpenClaw, webhook, or ntfy destinations.

Mitigation: Use callback destinations you control and avoid sending sensitive work through webhook or ntfy callbacks.

Risk: Team mode writes a Claude Stop hook and updates project Claude settings.

Mitigation: Review existing .claude hooks and settings before use, and run in a project where hook changes can be inspected or reverted.

Risk: Task content, session state, and debug details may be written under /tmp during execution.

Mitigation: Avoid sensitive prompts and clean temporary session or debug files after runs where confidentiality matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deadlining/skills/fast-claude-code)
- [ClawHub publisher profile](https://clawhub.ai/user/deadlining)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with shell command examples, callback summaries, and optional generated code, reports, or configuration changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs Claude Code through tmux; Team mode can create Markdown reports and update Claude project hook configuration.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
