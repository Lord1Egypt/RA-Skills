## Description: <br>
Comind guides an AI member through CoMind collaboration workflows for task execution, Markdown synchronization, chat collaboration, scheduled checks, and status reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dqalex](https://clawhub.ai/user/dqalex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI operators use this skill to let an agent participate in a CoMind workspace, including accepting task pushes, updating task and delivery records, synchronizing Markdown documents, responding in project or task chats, and reporting heartbeat status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a CoMind API token to modify shared project, task, delivery, and status data. <br>
Mitigation: Use a least-privilege scoped token, install only in a dedicated CoMind workspace, and review operations before enabling automated updates. <br>
Risk: Markdown synchronization and heartbeat workflows may read local workspace context and push updates silently. <br>
Mitigation: Confirm which directories and CoMind records the skill may read or modify before enabling sync, heartbeat, or scheduled workflows. <br>
Risk: A misconfigured COMIND_BASE_URL could send workspace data or tokens to an unintended service. <br>
Mitigation: Verify COMIND_BASE_URL points to a trusted CoMind instance and avoid exposing COMIND_API_TOKEN in chat, logs, or synced Markdown. <br>


## Reference(s): <br>
- [Comind ClawHub listing](https://clawhub.ai/dqalex/comind) <br>
- [CoMind homepage](https://github.com/comind) <br>
- [CoMind AI member manual](artifact/SKILL.md) <br>
- [Task push template](artifact/references/task-push.md) <br>
- [Task board template](artifact/references/task-board.md) <br>
- [Document delivery template](artifact/references/deliveries.md) <br>
- [Schedule template](artifact/references/schedules.md) <br>
- [System information template](artifact/references/system-info.md) <br>
- [Heartbeat progress check](artifact/references/heartbeat-check-progress.md) <br>
- [Heartbeat CoMind sync](artifact/references/heartbeat-sync-to-comind.md) <br>
- [Heartbeat daily report](artifact/references/heartbeat-daily-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with JSON action examples, shell command snippets, and document templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COMIND_BASE_URL and COMIND_API_TOKEN for CoMind API interactions.] <br>

## Skill Version(s): <br>
2.3.4 (source: server release metadata; artifact frontmatter and changelog mention 2.2.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
