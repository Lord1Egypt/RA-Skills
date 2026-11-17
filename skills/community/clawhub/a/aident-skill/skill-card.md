## Description:

Use Aident from agent environments to discover, verify, and operate connected integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aident-ai](https://clawhub.ai/user/aident-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let agents discover Aident Loadout capabilities, check Vault connection state, operate connected SaaS and API integrations, configure MCP access, and fall back to OpenAPI workflows when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to operate broad third-party work integrations and execute actions in connected accounts.

Mitigation: Use accounts appropriate for delegation, verify live schemas and Vault connection state before execution, prefer read-only discovery first, and review audit history for completed actions.

Risk: Setup and install instructions rely on mutable remote resources and package commands.

Mitigation: Review setup instructions before use and prefer pinned, reviewed install and MCP commands for managed environments.

Risk: REST examples and test scripts use bearer tokens and credential files.

Mitigation: Do not run token-handling scripts with production tokens unless the endpoint is trusted, avoid printing secrets, and use Aident-managed OAuth or Vault flows when available.

## Reference(s):

- [Aident Loadout Reference](references/loadout.md)
- [MCP Client Setup](references/mcp.md)
- [OpenAPI Reference](references/api.md)
- [Troubleshooting](references/troubleshooting.md)
- [Aident Loadout](https://loadout.aident.ai)
- [Aident Documentation](https://docs.aident.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline bash, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to execute CLI, MCP, or OpenAPI operations against user-authorized Aident Loadout integrations.]

## Skill Version(s):

0.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
