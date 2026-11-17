## Description:

Automate Basecamp project management, to-dos, messages, people, and to-do list organization via Rube MCP (Composio). Always search tools first for current schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to automate Basecamp project work through Rube MCP, including creating and organizing to-do lists, posting messages, managing people and access, and inspecting project structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to make real Basecamp project, message, task, people, and access changes through the user's connected account.

Mitigation: Review each requested write or access-management action before execution, especially publishing messages, notifying subscribers, creating users, or granting and revoking project access.

Risk: Using stale tool schemas or unresolved IDs can create Basecamp items in the wrong project section or apply access changes to the wrong people.

Mitigation: Search current Rube tool schemas first and resolve project, to-do set, to-do list, message board, and person IDs before performing write operations.

## Reference(s):

- [Rube MCP endpoint](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with tool sequences, parameter notes, and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active Rube MCP connection and Basecamp authorization; Basecamp rich text fields use HTML.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
