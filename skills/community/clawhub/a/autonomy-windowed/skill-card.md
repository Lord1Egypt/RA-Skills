## Description: <br>
Time-windowed autonomous task queue that limits autonomous work to configured active hours, uses overnight standby for cron maintenance, and provides queue, heartbeat, checkpoint, and logging templates for predictable schedules and token budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luciusrockwing](https://clawhub.ai/user/luciusrockwing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an autonomous agent to pull work from a queue only during defined time windows, with overnight standby behavior, cron coordination, and progress logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad scheduled autonomy can let an agent select and perform queued work without enough task boundaries. <br>
Mitigation: Define allowed task categories in the queue and require approval before destructive, external, account-affecting, or high-cost actions. <br>
Risk: Urgent override behavior can trigger work outside the configured autonomy window. <br>
Mitigation: Limit what qualifies as urgent and require human confirmation for off-hours urgent work unless the task is explicitly pre-approved. <br>
Risk: Persistent checkpoint, memory, learning, and goal-writing behavior can store sensitive or unwanted project context. <br>
Mitigation: Review writable paths, restrict memory/checkpoint contents, and remove or replace the hard-coded MONEY goal before enabling the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luciusrockwing/autonomy-windowed) <br>
- [Checkpoint Formats - Context Protection](references/checkpoints.md) <br>
- [Windowed Autonomy Heartbeat Template](templates/HEARTBEAT.md) <br>
- [Task Queue Template](templates/QUEUE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown templates and procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces queue, heartbeat, checkpoint, memory, and progress-log structures for scheduled autonomous agent work.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
