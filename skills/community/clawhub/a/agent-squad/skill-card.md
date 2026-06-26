## Description: <br>
Agent Squad manages persistent AI coding squads in tmux sessions with task queues, progress reports, watchdog restarts, and support for Claude Code, Codex, Gemini CLI, OpenCode, Kimi, Trae, Aider, and Goose. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xTimi](https://clawhub.ai/user/0xTimi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to launch, assign work to, monitor, ping, stop, restart, and archive persistent AI coding squads that operate on project repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts unattended AI coding agents with broad access to the selected project directory. <br>
Mitigation: Use isolated repositories, disposable worktrees, or separate branches; keep .env files, API keys, private keys, and sensitive customer data out of squad project directories; review commits before merging. <br>
Risk: Status and peek operations may expose live terminal contents from an active squad session. <br>
Mitigation: Use the skill only with trusted operators and avoid running squads in terminals or project directories that may reveal secrets or sensitive customer data. <br>
Risk: Watchdog behavior can restart crashed squads and continue autonomous work after an interruption. <br>
Mitigation: Stop squads when they should no longer run and verify active squad status before leaving unattended work enabled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xTimi/agent-squad) <br>
- [Project Homepage](https://github.com/0xTimi/agent-squad) <br>
- [Support Issues](https://github.com/0xTimi/agent-squad/issues) <br>
- [Agent Squad Guide](docs/guide.md) <br>
- [Supported AI Engines](references/engines.md) <br>
- [tmux](https://github.com/tmux/tmux) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell command execution and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can start or control tmux sessions and background AI engine processes when the user requests squad operations.] <br>

## Skill Version(s): <br>
0.9.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
