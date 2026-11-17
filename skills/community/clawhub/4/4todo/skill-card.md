## Description:

Manage 4todo (4to.do) from chat. Capture tasks, prioritize with the Eisenhower Matrix, reorder, complete, and manage recurring tasks across workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackstorm](https://clawhub.ai/user/blackstorm)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage 4todo workspaces, todos, priorities, ordering, completion state, and recurring tasks from an agent chat interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real 4todo token can be exposed locally through documented command usage.

Mitigation: Use a narrowly scoped, revocable token where available, inject it through environment configuration, and avoid shared hosts where process arguments may be visible to other users.

Risk: The skill can change account data by creating, completing, reordering, updating, or deleting todos and recurring todos.

Mitigation: Confirm account-changing actions before execution, especially recurring-task deletion or schedule changes, and re-fetch the affected workspace to verify the result.

Risk: Expired or invalid tokens can trigger repeated failed API calls if handled incorrectly.

Mitigation: Stop retrying on 401 invalid_token or token_expired responses and ask the user to refresh the token in configuration.

## Reference(s):

- [4todo ClawHub listing](https://clawhub.ai/blackstorm/skills/4todo)
- [4todo app](https://4to.do)
- [4todo API v0 documentation](references/api_v0.md)
- [4todo API v0 base URL](https://4to.do/api/v0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with optional curl commands, JSON snippets, and configuration examples when technical detail is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a FOURTODO_API_TOKEN bearer token and curl to interact with the 4todo API; user-facing responses should avoid exposing internal IDs unless needed for disambiguation.]

## Skill Version(s):

0.1.3 (source: server release metadata, released 2026-02-07T13:09:01Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
