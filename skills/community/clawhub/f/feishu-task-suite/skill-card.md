## Description: <br>
Feishu Task Suite helps an agent create, query, update, delete, complete, and organize Feishu tasks and task lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external Feishu users can use this skill to let an agent manage tasks and task lists under their Feishu identity. It is suited for creating tasks, listing or retrieving task details, completing or reopening tasks, changing due dates, creating task lists, viewing list tasks, and adding task-list members. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad task-related trigger words could activate the skill when a user mentions tasks generically. <br>
Mitigation: Confirm that the user intends to manage Feishu tasks before creating, updating, deleting, completing, sharing, or listing task data. <br>
Risk: The skill can change tasks and task lists under the user's Feishu identity, including members and completion status. <br>
Mitigation: Confirm the target task or task list, affected members, due dates, and intended action before allowing changes. <br>
Risk: Created tasks may be hard to edit later if the current user is not included as a member. <br>
Mitigation: Pass current_user_id from the message context when creating tasks so the tool can add the current user as a follower when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3152557994-ship-it/feishu-task-suite) <br>
- [Publisher profile](https://clawhub.ai/user/a3152557994-ship-it) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu task and task-list identifiers such as task_guid and tasklist_guid.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
