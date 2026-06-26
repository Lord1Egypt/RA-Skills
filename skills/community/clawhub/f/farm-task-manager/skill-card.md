## Description: <br>
Manage daily, weekly, and seasonal farm chores with task scheduling, priorities, status updates, recurring tasks, filtering, and export options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johstracke](https://clawhub.ai/user/johstracke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Farmers, homesteaders, and farm-to-table operators use this skill to manage local farm chores, recurring work, priorities, assignees, and task exports from a command-line task list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task notes and exports may contain sensitive farm, worker, or operational details. <br>
Mitigation: Avoid storing secrets in task notes and review Markdown or JSON exports before sharing. <br>
Risk: Exports write files under the user's home directory and may overwrite an existing file. <br>
Mitigation: Choose export paths deliberately and check the destination before running export commands. <br>


## Reference(s): <br>
- [Farm Task Manager ClawHub listing](https://clawhub.ai/johstracke/farm-task-manager) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Command-line guidance with local task data and optional Markdown or JSON exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores tasks locally under ~/.openclaw/workspace/farm-task-manager/tasks.json and can export filtered task lists to user-selected files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
