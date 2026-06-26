## Description: <br>
Dida365 helps agents query and manage TickTick/Dida365 tasks, projects, to-dos, productivity stats, completion status, and filtered task views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangcheng](https://clawhub.ai/user/huangcheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and productivity-focused teams use this skill to let an agent inspect, search, create, update, move, and complete TickTick/Dida365 tasks and lists through configured MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, move, batch-add, and complete tasks in a connected TickTick/Dida365 account. <br>
Mitigation: Require user confirmation before write actions, especially for bulk changes or work-related lists. <br>
Risk: Broad activation around task-management requests may expose personal or work task data to the agent. <br>
Mitigation: Install only when the user intends the assistant to access TickTick/Dida365, and avoid using it for accounts or lists that should remain private. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [Natural-language responses with MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or modify task data in the connected TickTick/Dida365 account.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
