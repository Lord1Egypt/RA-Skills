## Description:

Creates Feishu reading tasks from trigger phrases by extracting conversation content and assigning the task to the conversation sender.

This skill is ready for commercial/non-commercial use.

## Publisher:

[partigle](https://clawhub.ai/user/partigle)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and Feishu users use this skill to save links, documents, and other conversation items into a personal to-read task list assigned to the conversation sender.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may cause the agent to create Feishu reading tasks from conversation content before the exact item, assignee, or content is confirmed.

Mitigation: Confirm the content, assignee, and task details before creating the Feishu task.

Risk: Task details may be recorded in memory/YYYY-MM-DD.md files.

Mitigation: Tell users where records are stored and define how those records are reviewed, retained, or deleted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/partigle/skills/feishu-reading-task)

## Skill Output:

**Output Type(s):** [JSON, Files, API Calls]

**Output Format:** [JSON task data and Markdown memory records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Feishu to-read task data assigned to the sender and may record task details in memory/YYYY-MM-DD.md.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
