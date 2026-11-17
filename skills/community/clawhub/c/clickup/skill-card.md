## Description:

Interact with the ClickUp project management platform via REST API for task management, reporting, workflow automation, pagination, subtasks, and common query patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shubhs0707](https://clawhub.ai/user/shubhs0707)

### License/Terms of Use:


## Use Case:

Developers, operators, and project teams use this skill to query, report on, create, and update ClickUp tasks through ClickUp REST API patterns and helper shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClickUp API tokens can expose or modify workspace data if overprivileged or shared.

Mitigation: Use the least-privileged ClickUp token available and avoid placing tokens in shared files, prompts, transcripts, or generated output.

Risk: Task creation, update, or deletion commands can change live ClickUp work items.

Mitigation: Require explicit approval before running POST, PUT, or DELETE operations against ClickUp.

Risk: Incomplete pagination or missing subtask parameters can produce misleading task reports.

Mitigation: Use subtasks=true for task queries and loop through pages until ClickUp reports last_page=true.

## Reference(s):

- [ClickUp API Reference](references/api-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, curl, jq, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ClickUp API requests and helper-script commands that require CLICKUP_API_KEY and CLICKUP_TEAM_ID.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
