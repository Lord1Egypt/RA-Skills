## Description:

Agentic Beehive MCP Server is an MCP coordination server that gives AI agents state awareness, branch routing, external colony management, alerts, and local coordination memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hon27hon](https://clawhub.ai/user/hon27hon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this MCP server to maintain local coordination state, choose task branches, register external data or agent endpoints, poll their status, and track alerts or evolution requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server can store local coordination state and poll arbitrary user-registered colony endpoints.

Mitigation: Run it in a restricted environment or network sandbox, and review or constrain allowed colony endpoints before exposing it to agents or users.

Risk: Agents may rely on branch, colony, alert, or evolution state that has been updated by other callers.

Mitigation: Review stored coordination state and scan the skill before deployment, especially in shared or multi-agent environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hon27hon/skills/agentic-beehive-mcp)
- [Publisher profile](https://clawhub.ai/user/hon27hon)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [MCP tool responses as JSON-like dictionaries, plus setup guidance and configuration snippets in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite state and may poll user-registered colony endpoints.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and README version entry)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
