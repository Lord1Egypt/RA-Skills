## Description:

Dida Coach helps agents turn goals into staged plans and time boxes, manage Dida365 tasks through MCP, and support reviews, commitment tracking, rescheduling, and follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siyuanfeng636-cpu](https://clawhub.ai/user/siyuanfeng636-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan, schedule, update, and review Dida365 tasks through natural-language coaching workflows. It is intended for goal breakdown, time-box creation, task CRUD, productivity-system summaries, and daily, weekly, or monthly review support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live Dida365 task changes from broad natural-language requests.

Mitigation: Review proposed task changes before execution, require confirmation for broad or high-impact updates, and verify created or updated tasks after write operations.

Risk: The optional local OAuth helper stores Dida365 credentials in a local environment file.

Mitigation: Prefer the normal MCP Connect/Authorize flow; if local OAuth is used, restrict permissions on ~/.dida-coach/dida-openapi.env and rotate or delete credentials if exposed.

Risk: The local productivity system writes summaries and planning files under the user's home directory.

Mitigation: Disclose the target path before initialization, require explicit confirmation for first-time setup, and avoid copying the full Dida task database into local files.

## Reference(s):

- [Dida Coach ClawHub release page](https://clawhub.ai/siyuanfeng636-cpu/skills/dida365-coach-skills)
- [Dida365 MCP client setup](references/mcp-client-setup.md)
- [Dida365 MCP tool routing](references/mcp-tool-routing.md)
- [Dida field semantics](references/dida-field-semantics.md)
- [Dida OpenAPI auth setup](references/openapi-auth-setup.md)
- [Dida365 MCP service](https://mcp.dida365.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, configuration examples, and task-change summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate Dida365 task reads or writes through MCP and may create local productivity files when the user has authorized the relevant workflow.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
