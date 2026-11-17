## Description:

Helps agents manage DingTalk Teambition projects and tasks, including querying todos, creating and updating tasks, adding comments or progress, uploading task files, looking up members, and managing sprints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qijian2026](https://clawhub.ai/user/qijian2026)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams that use Teambition can use this skill to query, create, update, comment on, and archive tasks and to inspect projects, members, statuses, custom fields, files, and sprints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify shared Teambition project and task data.

Mitigation: Require explicit confirmation before archive, restore, sprint lifecycle changes, bulk updates, or file uploads, and review proposed changes before execution.

Risk: Teambition workspace data and member profile details may appear in logs or agent transcripts.

Mitigation: Use the least-privileged account available, limit result sharing, and avoid exposing raw IDs, email addresses, phone numbers, employee numbers, or signed file links unless needed.

Risk: A Teambition user token grants access to workspace data and actions.

Mitigation: Prefer an environment variable or secret manager for the token and do not commit user-token.json.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qijian2026/skills/dingtalk-teambition-project)
- [Teambition Open Platform](https://open.teambition.com/)
- [Teambition User Token](https://open.teambition.com/user-mcp)
- [Task TQL Reference](references/tql.md)
- [Project TQL Reference](references/project-tql.md)
- [Task Operations Reference](references/task-ops.md)
- [Project Operations Reference](references/project-ops.md)
- [Error Handling Reference](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and structured task or project summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEAMBITION_USER_TOKEN and local python3/uv runtime availability.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
