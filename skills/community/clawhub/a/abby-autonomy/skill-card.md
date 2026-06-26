## Description: <br>
Enables Abby to proactively pull tasks from a local queue, track progress, and continue work until completion or resource limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earnabitmore365](https://clawhub.ai/user/earnabitmore365) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers or operators using Abby use this skill to maintain a local Markdown task queue and task-state file so the agent can select ready tasks, resume running work, and record completion or blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous work can be steered by whoever can edit the local task queue. <br>
Mitigation: Keep tasks/QUEUE.md writable only by trusted users and review the queue before enabling cron or heartbeat automation. <br>
Risk: Task names or state files may accidentally contain sensitive information. <br>
Mitigation: Avoid putting secrets, credentials, or private account details in task names, queue entries, or memory/task_state.json. <br>
Risk: Queued tasks may affect accounts, finances, external services, or important files. <br>
Mitigation: Require manual approval before allowing the skill to act on high-impact tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earnabitmore365/abby-autonomy) <br>
- [Skill documentation](SKILL.md) <br>
- [Task queue template](tasks/QUEUE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown task queue updates, JSON task-state updates, and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local task status in memory/task_state.json and local task queue state in tasks/QUEUE.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
