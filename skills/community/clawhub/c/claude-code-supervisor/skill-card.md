## Description:

Supervise Claude Code sessions running in tmux with Claude Code hooks, bash pre-filtering, fast LLM triage, notifications, and watchdog checks for errors, stuck agents, and task completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johba37](https://clawhub.ai/user/johba37)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent-harness operators use this skill to monitor long-running Claude Code sessions in tmux, classify failures or completion states, nudge sessions when appropriate, and notify a human or harness when attention is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs automatic hooks that can run project-configured triage and notification commands.

Mitigation: Review the skill before installing, use it only in trusted repositories and environments, inspect any existing .claude-code-supervisor.yml, and avoid arbitrary triage.command or notify.command values.

Risk: Notifications and triage can forward paths, prompts, error output, and task context to configured LLM or notification backends.

Mitigation: Do not send notifications to external services unless sharing that context is acceptable for the project.

Risk: Supervisor actions may involve permission prompts or potentially destructive actions.

Mitigation: Require human approval for permission prompts and destructive actions, and follow the escalation rules for repeated errors, credential requests, or ambiguous states.

Risk: The watchdog and generated helper behavior can rely on temporary files or fixed /tmp helper paths.

Mitigation: Run the watchdog as a normal user and avoid fixed /tmp helpers where possible.

## Reference(s):

- [Escalation Rules](artifact/references/escalation-rules.md)
- [State Detection Patterns](artifact/references/state-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/johba37/skills/claude-code-supervisor)
- [The Five Levels from Spicy Autocomplete to the Software Factory](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux and a Claude CLI-compatible command; optional notification backends and watchdog scheduling depend on local configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
