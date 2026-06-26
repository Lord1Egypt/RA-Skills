## Description: <br>
Codex Agent Enhanced lets OpenClaw operate OpenAI Codex CLI for task execution, knowledge-base maintenance, configuration management, and asynchronous monitoring through tmux, notify hooks, and pane monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geq1fan](https://clawhub.ai/user/geq1fan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical teams use this skill to delegate Codex CLI workflows to OpenClaw: clarify requirements, craft prompts, run Codex, monitor progress, handle approvals, check quality, and report results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently run Codex hooks and send Codex completion content to Telegram. <br>
Mitigation: Enable it only when Codex/OpenClaw automation is intended, set notification routing explicitly, and minimize or disable notifications for confidential repositories. <br>
Risk: Risky default routing values and bot account mappings can send messages to an unintended Telegram destination. <br>
Mitigation: Replace sample chat IDs and bot account names before use, then verify delivery with a non-sensitive test task. <br>
Risk: Long session-retention and cron options can keep automation active beyond a single task. <br>
Mitigation: Review session-retention and cron settings before enabling them, use project-scoped state files, and disable cron when it is not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/geq1fan/codex-agent-enhanced) <br>
- [README_EN.md](README_EN.md) <br>
- [INSTALL.md](INSTALL.md) <br>
- [Codex CLI Reference](references/codex-cli-reference.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenAI Codex CLI](https://github.com/openai/codex) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce prompts, operational checklists, Codex commands, hook configuration, and task-status guidance.] <br>

## Skill Version(s): <br>
1.0.0-enhanced (source: server release metadata and CHANGELOG.md, released 2026-03-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
