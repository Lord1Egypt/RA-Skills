## Description: <br>
Agent Ops provides runtime monitoring and recovery guidance for AI coding agent sessions, including rate-limit recovery, context usage estimation, stale-session recovery, checkpoint and rollback patterns, token budgets, and model fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage active AI coding agent sessions, recover from rate limits or stale sessions, protect repositories before risky shell commands, and keep context and model usage under control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional daemon and transcript-recovery patterns can read sensitive transcripts, thinking blocks, or recovered notes. <br>
Mitigation: Scope recovery to known sessions, redact archived material, set retention limits, and avoid storing raw transcripts or thinking blocks. <br>
Risk: Rate-limit recovery can send keys to tmux panes and may resume the wrong prompt if enabled broadly. <br>
Mitigation: Do not enable global recovery; re-check pane contents, confirm the session is still rate-limited, and block confirmation prompts before sending keys. <br>
Risk: Checkpoint and rollback hooks can mutate repository state when destructive commands fail. <br>
Mitigation: Limit hooks to trusted repositories, require confirmation for destructive commands, log actions, and inspect checkpoints before applying rollback. <br>


## Reference(s): <br>
- [Rate Limit Recovery Pattern](references/04-rate-limit.md) <br>
- [Context Usage Estimation Pattern](references/05-context-estimation.md) <br>
- [Stale Session Daemon Pattern](references/17-stale-session-daemon.md) <br>
- [Checkpoint and Rollback Pattern](references/19-checkpoint-rollback.md) <br>
- [Token Budget Pattern](references/20-token-budget.md) <br>
- [Model Fallback Pattern](references/21-model-fallback.md) <br>
- [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks) <br>
- [Oh My Claude Code](https://github.com/Yeachan-Heo/oh-my-claudecode) <br>
- [Continuous Claude v3](https://github.com/parcadei/Continuous-Claude-v3) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes one shell script for transcript token usage and operational patterns for hooks, cron, tmux, and git checkpoint workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
