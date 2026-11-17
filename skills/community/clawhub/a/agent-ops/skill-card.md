## Description:

Agent Ops provides runtime monitoring and recovery patterns for AI coding-agent sessions, including context token checks, rate-limit recovery, stale-session handling, checkpoint and rollback guidance, token budgeting, and model fallback guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor long-running coding-agent sessions, recover from rate limits or stale sessions, manage context pressure, and prepare rollback patterns before risky shell operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript scavenging or stale-session recovery can retain sensitive session content.

Mitigation: Enable those patterns only with explicit opt-in, private file permissions, secret redaction, and retention limits.

Risk: Automatic rollback or recovery hooks can change repository or session state unexpectedly.

Mitigation: Review each hook before enabling it, require confirmation before state-changing actions, and test rollback and error handling in a disposable repository.

Risk: Rate-limit recovery can send input to an active tmux pane at the wrong time.

Mitigation: Re-check the pane content immediately before sending input and block recovery when confirmation, deletion, overwrite, or force-push prompts are visible.

## Reference(s):

- [Rate Limit Detection and Recovery](references/04-rate-limit.md)
- [Lightweight Context Usage Estimation](references/05-context-estimation.md)
- [Stale Session Daemon](references/17-stale-session-daemon.md)
- [Git Checkpoint and Auto Rollback](references/19-checkpoint-rollback.md)
- [Token Budget Per Subtask](references/20-token-budget.md)
- [Auto Model Fallback](references/21-model-fallback.md)
- [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks)
- [Oh My ClaudeCode](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [Continuous Claude v3](https://github.com/parcadei/Continuous-Claude-v3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash snippets and one shell script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included context-usage script prints an input-token count when available and otherwise emits no output.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
