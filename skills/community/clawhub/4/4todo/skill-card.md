## Description: <br>
Manage 4todo (4to.do) from chat. Capture tasks, prioritize with the Eisenhower Matrix, reorder, complete, and manage recurring tasks across workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blackstorm](https://clawhub.ai/user/blackstorm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage 4todo workspaces, todos, priorities, ordering, completion state, and recurring tasks from an agent chat workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a bearer token to read and modify a user's 4todo account. <br>
Mitigation: Provide the API token through OpenClaw configuration, environment injection, or a secret store rather than chat, logs, or repo files. <br>
Risk: Agent actions can create, complete, reorder, or update recurring todos in the selected workspace. <br>
Mitigation: Review workspace and task names before broad changes or recurring-task updates, then re-fetch tasks to verify the result. <br>
Risk: Expired or invalid tokens can cause repeated failed API calls. <br>
Mitigation: Stop retrying on token_expired or invalid_token responses and ask the user to refresh the token in 4todo settings and update configuration. <br>


## Reference(s): <br>
- [4todo Skill Page](https://clawhub.ai/blackstorm/4todo) <br>
- [4todo Website](https://4to.do) <br>
- [4todo API v0 Documentation](references/api_v0.md) <br>
- [4todo API v0 Base URL](https://4to.do/api/v0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with task summaries, configuration guidance, and optional curl commands when debugging or requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-provided FOURTODO_API_TOKEN and should avoid exposing internal IDs or secrets by default.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
