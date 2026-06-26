## Description: <br>
Interact with FlowDeck Project Management API (projects, cycles, tasks). Use for CRUD + archive/unarchive operations via the FlowDeck REST API through Supabase Edge Functions. Trigger when user asks about project status, cycle progress, task management, or implementing work from a Flow task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araujodgdev](https://clawhub.ai/user/araujodgdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project operators use this skill to inspect FlowDeck project status, summarize active cycles and task progress, and create or update project-management records through the FlowDeck REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify live FlowDeck workspace data using a bearer API key. <br>
Mitigation: Use a scoped, revocable API key through FLOWBOARD_API_KEY when possible, verify the base URL, and review intended operations before execution. <br>
Risk: Delete, archive, broad update, or task-driven implementation actions can affect project records or downstream work. <br>
Mitigation: Confirm ambiguous or destructive targets, double-check IDs and payloads, and prefer narrow updates over broad changes. <br>


## Reference(s): <br>
- [Flow PMS on ClawHub](https://clawhub.ai/araujodgdev/flow-pms) <br>
- [FlowBoard API summary](references/openapi-summary.md) <br>
- [Fluxos praticos em PT-BR](references/workflows-ptbr.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live FlowDeck API mutations when the user authorizes create, update, delete, archive, or unarchive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
