## Description:

Preserve approved agent context, report work status and service incidents or needs, and use a personal Agent Yurt cloud when its MCP connection and scoped access are configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solvopus-tech](https://clawhub.ai/user/solvopus-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users use this skill to preserve owner-approved context in an authorized Agent Yurt space, report concise work status, and prepare reviewed handoffs or recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is marked benign with medium confidence but is incomplete because several local references could not be resolved.

Mitigation: Review the unresolved references and the skill instructions before installing.

Risk: Backup and recovery workflows can involve private owner data and credentials.

Mitigation: Use only owner-approved files and granted scopes, keep credentials in a secret manager, and review recovery plans before applying them.

## Reference(s):

- [GitHub source (skills/agent-yurt)](https://github.com/Solvopus-Tech/agent-yurt-integrations/tree/main/skills/agent-yurt)
- [Agent Yurt MCP setup guide](https://agentyurt.com/guides/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Files, Configuration instructions]

**Output Format:** [Markdown guidance, MCP tool calls, shell commands, and portable snapshot or configuration content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions depend on owner-approved files, configured connections, and granted scopes.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
