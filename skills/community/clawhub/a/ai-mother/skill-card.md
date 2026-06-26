## Description: <br>
AI Mother monitors and manages local AI coding agents such as Claude Code, Codex, OpenCode, and Aider by checking execution status, diagnosing stuck sessions, sending recovery inputs, and escalating owner decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guguoyi](https://clawhub.ai/user/guguoyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams running local AI coding agents use this skill to monitor agent status, inspect stuck sessions, coordinate safe recovery actions, and route permission decisions or completion notices to the owner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent supervision can inspect AI sessions and sensitive local context. <br>
Mitigation: Install only in workspaces where this visibility is acceptable, and review conversation logs, local state files, and configuration before enabling patrols. <br>
Risk: The skill can send inputs to running agents and influence active work. <br>
Mitigation: Keep owner approval for elevated permissions, destructive commands, credentials, external communications, and other sensitive requests. <br>
Risk: Cron patrols and Feishu notifications create ongoing monitoring and external owner alerts. <br>
Mitigation: Review scheduled patrol jobs and the configured Feishu recipient before use, and remove cron jobs when monitoring is no longer needed. <br>
Risk: Broad auto-heal or duplicate cleanup can affect active agent sessions. <br>
Mitigation: Avoid automatic cleanup in sensitive workspaces; inspect detected issues and use dry-run or manual handling when available. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [AI Butler Reference Guide](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local state, SQLite history, cron patrols, and Feishu owner notifications when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
