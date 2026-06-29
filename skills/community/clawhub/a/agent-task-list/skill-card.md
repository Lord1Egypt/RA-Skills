## Description: <br>
Agent Task List creates isolated task queues for each agent, supporting task assignment, status updates, progress tracking, history, priority scheduling, and state synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wljmmx](https://clawhub.ai/user/wljmmx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage independent task queues for agents, including assignment, lifecycle updates, priority scheduling, retries, history, and task statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A shared local task registry can expose task names, descriptions, status, and history across agents in the same OpenClaw workspace. <br>
Mitigation: Use the skill only with mutually trusted agents and avoid storing sensitive operational details in task names or descriptions. <br>
Risk: Persistent task-list and history files can retain operational details after tasks are completed, failed, or retried. <br>
Mitigation: Review local retention needs and clear task and history files according to workspace policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wljmmx/agent-task-list) <br>
- [Publisher Profile](https://clawhub.ai/user/wljmmx) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists task lists, indexes, and history in local OpenClaw workspace files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
