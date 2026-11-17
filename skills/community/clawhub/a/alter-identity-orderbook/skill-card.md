## Description:

Use when an agent has an ongoing, standing need for people matching specific trait ranges, rather than a single one-off search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[true-alter](https://clawhub.ai/user/true-alter)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to create, inspect, cancel, and poll standing identity-trait requirements through the ~alter hosted MCP service. It is for ongoing matching workflows where eligible people must opt in before they can appear in standing matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid polling can spend money when a fill is delivered.

Mitigation: Confirm a polling budget before paid identity reveals and stop polling when the budget is reached.

Risk: Standing requirements create server-side state that may persist after the immediate task.

Mitigation: Use expirations when creating requirements and cancel requirements when the standing need is finished.

Risk: The integration requires an authenticated ALTER_API_KEY.

Mitigation: Set a real operator-approved key and avoid placeholder, guessed, or unattended credential use.

## Reference(s):

- [~Alter MCP server](https://mcp.truealter.com/api/v1/mcp)
- [ClawHub skill page](https://clawhub.ai/true-alter/skills/alter-identity-orderbook)
- [~alter publisher profile](https://clawhub.ai/user/true-alter)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls]

**Output Format:** [Markdown guidance with MCP tool names, configuration details, and operational cautions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALTER_API_KEY for authenticated ~alter MCP operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
