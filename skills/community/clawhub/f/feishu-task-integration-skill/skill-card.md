## Description: <br>
Synchronizes local to-do items with Feishu Tasks, including task creation, deadline parsing, assignee setup, and completion status updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showdownagain](https://clawhub.ai/user/showdownagain) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect local to-do workflows with Feishu Tasks, create tasks from short commands, assign responsible users, set deadlines from natural-language time expressions, and sync completion status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, create, assign, follow, and complete Feishu tasks when configured with a Feishu app that has task and member-management permissions. <br>
Mitigation: Install only when that access is intended, grant the Feishu app the narrowest scopes required, and verify assignees and followers before enabling sync. <br>
Risk: The server security guidance flags hardcoded user IDs and fixed /home/gary paths in the artifact. <br>
Mitigation: Remove hardcoded user IDs, replace fixed local paths with user-controlled configuration, and review the effective configuration before use. <br>
Risk: Task text, API payloads, and task identifiers may be logged or stored locally while syncing with Feishu. <br>
Mitigation: Avoid sensitive task content unless external Feishu sync and local persistence are acceptable, and redact or disable verbose payload logging in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/showdownagain/feishu-task-integration-skill) <br>
- [Feishu task API guide](artifact/references/api_guide.md) <br>
- [Feishu integration configuration guide](artifact/references/configuration.md) <br>
- [Feishu task API base](https://open.feishu.cn/open-apis/task/v2/) <br>
- [Feishu developer console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code, shell commands, JSON configuration snippets, and Feishu API references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu tasks and local todo_data.json when used with valid Feishu credentials and configured user IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
