## Description: <br>
Interact with ClickUp project management platform via REST API. Use when working with tasks, spaces, lists, assignees, or any ClickUp workflow automation. Handles pagination, subtasks, and common query patterns. Use for task management, reporting, automation, or any ClickUp-related queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shubhs0707](https://clawhub.ai/user/shubhs0707) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to query, report on, create, and update ClickUp tasks through the ClickUp REST API. It is suited for task management automation that needs pagination, subtasks, assignee reporting, and workspace/list filtering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent access private ClickUp workspace data through the ClickUp API. <br>
Mitigation: Use the least-privileged ClickUp token available and configure only the team, space, and list IDs needed for the intended workflow. <br>
Risk: Create, update, or delete task operations can modify project records. <br>
Mitigation: Require explicit confirmation before task-changing API calls and verify target task, team, list, and status values before execution. <br>


## Reference(s): <br>
- [ClickUp API Reference](references/api-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/shubhs0707/clickup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLICKUP_API_KEY and CLICKUP_TEAM_ID environment variables for live ClickUp API calls.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
