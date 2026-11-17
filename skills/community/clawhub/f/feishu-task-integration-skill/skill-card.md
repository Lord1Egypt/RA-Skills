## Description:

Synchronizes local to-do items with Feishu Tasks by creating tasks, parsing natural-language deadlines, assigning owners, and updating completion status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showdownagain](https://clawhub.ai/user/showdownagain)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to connect an agent-managed local todo workflow with Feishu Tasks, including task creation, due-date handling, assignment, listing, and completion synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task titles, descriptions, due dates, assignees, and completion actions may be sent to Feishu.

Mitigation: Use only approved task data and an approved Feishu tenant, and confirm that users understand the external synchronization behavior before enabling the skill.

Risk: Hardcoded Feishu Open IDs or named default recipients can route tasks to an unintended user.

Mitigation: Remove hardcoded recipient IDs and require explicit assignee and follower configuration or confirmation before task creation.

Risk: Raw API response logging and broad task listing can expose task data beyond the intended scope.

Mitigation: Disable raw API response logging, scope task listing to the intended user, and review logs for sensitive task content.

Risk: Credential and configuration file handling may expose Feishu app secrets.

Mitigation: Store credentials in environment variables or a managed secret store, keep local config files out of version control, and rotate app secrets if exposure is suspected.

## Reference(s):

- [Feishu Task API Guide](artifact/references/api_guide.md)
- [Feishu Task Integration Configuration Guide](artifact/references/configuration.md)
- [Feishu Open Platform App Console](https://open.feishu.cn/app)
- [Feishu Tasks API v2](https://open.feishu.cn/open-apis/task/v2/)
- [ClawHub Skill Page](https://clawhub.ai/showdownagain/skills/feishu-task-integration-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown and plain-text agent responses with Python scripts and JSON configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Feishu API calls that create, list, or complete tasks when configured with valid credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
