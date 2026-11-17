## Description:

Use the BitsWeave MCP server to read shared project context and save durable work for other agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsweave](https://clawhub.ai/user/bitsweave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate work through BitsWeave by reading shared project context and saving durable notes, decisions, tasks, and documents for other agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared project context, coordination notes, decisions, tasks, and documents may be sent to the BitsWeave remote MCP service.

Mitigation: Install only in projects where sending that material to BitsWeave is acceptable, and confirm workspace and project boundaries before use.

Risk: OAuth authorization may grant the integration access to project context in the selected workspace.

Mitigation: Review the OAuth prompt before authorizing and avoid enabling the skill for private or sensitive material outside the intended BitsWeave workspace.

## Reference(s):

- [BitsWeave MCP endpoint](https://bitsweave.com/api/mcp)
- [ClawHub skill page](https://clawhub.ai/bitsweave/skills/bitsweave)
- [Publisher profile](https://clawhub.ai/user/bitsweave)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, Configuration]

**Output Format:** [Markdown guidance and MCP tool interactions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OAuth with the BitsWeave MCP service when tool calls require authorization.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
