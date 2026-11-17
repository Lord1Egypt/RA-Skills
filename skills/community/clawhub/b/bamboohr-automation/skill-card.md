## Description:

Automate BambooHR tasks via Rube MCP (Composio): employees, time-off, benefits, dependents, employee updates. Always search tools first for current schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

HR operations users and developers use this skill to guide BambooHR workflows through Rube MCP, including employee lookup, employee changes, time-off management, dependents, and benefits coverage tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive HR records, including employee and dependent PII.

Mitigation: Install only for authorized BambooHR users, request the minimum fields needed, and avoid displaying unnecessary PII in agent responses.

Risk: The skill can change employee records or time-off request status.

Mitigation: Require the agent to verify the exact employee or request, summarize intended changes, and obtain explicit confirmation before performing updates.

## Reference(s):

- [Rube MCP server](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with tool sequences, parameter notes, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active Rube MCP BambooHR connection and current tool schema lookup before use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
