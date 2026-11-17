## Description:

Manage Feishu tasks by creating, listing, completing, commenting, and organizing to-dos with assignees, due dates, and checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and knowledge workers use this skill to manage Feishu/Lark tasks from an AI agent, including task creation, querying, completion, comments, assignees, due dates, and checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Feishu App Secret could be exposed if pasted into chat logs, repositories, or unprotected configuration.

Mitigation: Store the App Secret in a protected config or secret store and avoid sharing real credentials in chats or source files.

Risk: The agent can create, complete, and comment on tasks in a Feishu workspace when granted write permissions.

Mitigation: Limit the Feishu app permissions to the task features needed and review create, complete, and comment actions before allowing workspace changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/a3152557994-ship-it/skills/feishu-task-mgr)
- [Feishu Open Platform](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline examples, JSON configuration snippets, and Feishu task-management actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured Feishu App ID and App Secret with task and comment permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-04-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
