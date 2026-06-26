## Description: <br>
Multi-agent AI coding swarm orchestration for planning parallel tasks, spawning Claude, Codex, and Gemini agents in tmux sessions with git worktrees, auto-reviewing, auto-integrating branches, and sending Telegram notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkbag](https://clawhub.ai/user/linkbag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to split coding work into approved parallel tasks, launch agent workers, monitor completion, and integrate results through scripted review and merge workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bypass approvals and automatically change, push, or merge repository content. <br>
Mitigation: Review scripts before use, run in a disposable or tightly controlled repository, and disable auto-endorsement, permission-bypass modes, and automatic push or merge behavior unless explicitly needed. <br>
Risk: Agent prompts, logs, notifications, or local OAuth and API credentials may expose sensitive information during orchestration. <br>
Mitigation: Avoid running the skill where credentials can affect protected branches, limit notification destinations, and review or reduce raw log retention before deployment. <br>


## Reference(s): <br>
- [AI Swarm Orchestration Skill Page](https://clawhub.ai/linkbag/ai-swarm) <br>
- [Swarm Lead - Heartbeat Checks](references/HEARTBEAT.md) <br>
- [Swarm Lead - Role Definition](references/ROLE.md) <br>
- [Swarm Lead - Tools Notes](references/TOOLS.md) <br>
- [Duty Table Template](references/duty-table-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce prompt files, task JSON, tmux/git commands, and operational status guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
