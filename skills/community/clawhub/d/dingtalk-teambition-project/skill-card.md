## Description: <br>
Helps agents query and manage Teambition projects, tasks, members, comments, attachments, task status, priority, assignees, and sprints through bundled scripts and TQL references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qijian2026](https://clawhub.ai/user/qijian2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, project contributors, and operations teams use this skill to inspect and update Teambition work items, find members and projects, manage sprints, and attach files or comments. It is intended for Teambition workflows, not for other project-management platforms or Git operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Teambition project and task data, including status, assignee, priority, sprint state, and archive or restore state. <br>
Mitigation: Require explicit user confirmation that names the exact target before destructive or high-impact changes such as archiving tasks, completing sprints, or changing status, assignee, or priority. <br>
Risk: The skill requires a Teambition user token that can grant access to account and workspace data. <br>
Mitigation: Prefer TEAMBITION_USER_TOKEN in the environment, keep any user-token.json file out of source control, and rotate the token if it is exposed. <br>
Risk: Task, member, and attachment queries can expose sensitive member details and signed download URLs. <br>
Mitigation: Minimize disclosure in responses and require explicit confirmation before returning attachment links or member contact details. <br>


## Reference(s): <br>
- [Teambition Open Platform](https://open.teambition.com/) <br>
- [Teambition User Token](https://open.teambition.com/user-mcp) <br>
- [TQL Reference](references/tql.md) <br>
- [Project TQL Reference](references/project-tql.md) <br>
- [Task Operations Reference](references/task-ops.md) <br>
- [Project Operations Reference](references/project-ops.md) <br>
- [Error Handling Reference](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown responses with inline shell commands, Teambition links, and tabular task summaries when listing multiple tasks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should resolve internal IDs to readable names before display and treat member details, tokens, and signed file links as sensitive.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
