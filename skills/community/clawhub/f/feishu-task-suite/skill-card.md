## Description:

Feishu Task Suite helps agents create, query, update, delete, and organize Feishu tasks and task lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to manage Feishu tasks and task lists, including creating tasks, listing pending work, updating status or due dates, and managing task-list membership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task changes can affect shared workflows or notify assignees, followers, and groups.

Mitigation: Confirm the target task or task list and any people or groups before creating, completing, deleting, assigning, or sharing.

Risk: Creating a task without the current user as a member can prevent later edits by that user.

Mitigation: Provide current_user_id from the message SenderId when creating tasks so the tool can add the creator as a follower.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, JSON, API calls]

**Output Format:** [Markdown guidance with JSON argument examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu task and task-list operation parameters such as task_guid, tasklist_guid, members, due, and completed_at.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
