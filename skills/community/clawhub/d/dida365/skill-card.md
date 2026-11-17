## Description:

Dida365 helps an agent interact with TickTick/Dida365 (滴答清单) to query, create, update, complete, search, and filter tasks, projects, and productivity statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangcheng](https://clawhub.ai/user/huangcheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent manage TickTick/Dida365 tasks and projects, including viewing lists, searching tasks, creating or updating tasks, completing tasks, and calculating completion rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can create, update, move, batch update, or complete tasks in the connected TickTick/Dida365 account.

Mitigation: Confirm task-system intent and review any create, batch update, move, or complete action before allowing it to run.

Risk: Generic task-management prompts could be routed to TickTick/Dida365 when the user intended a different task system.

Mitigation: Ask the user to confirm TickTick/Dida365 should be used before taking account actions for ambiguous task-management requests.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with MCP tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses mcp__dida__* tools for task-management read and write actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
