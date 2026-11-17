## Description:

Gate Exchange sub-account management skill for managing, creating, locking, unlocking, and listing Gate sub-accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

Gate users and account operators use this skill to list Gate sub-accounts, inspect sub-account status, and create, lock, or unlock normal sub-accounts through the Gate MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial sub-account write actions can change account access and trading availability.

Mitigation: Require explicit user confirmation before create, lock, or unlock actions and verify final status after the action.

Risk: The release relies on external Gate MCP setup and changeable runtime rules.

Mitigation: Review the Gate MCP setup before installation and verify or vendor the referenced runtime rules for the deployed environment.

Risk: API keys or raw API errors could expose sensitive account information.

Mitigation: Avoid exposing API keys and sanitize raw API errors before showing responses to end users.

## Reference(s):

- [Gate Sub-Account MCP Specification](references/mcp.md)
- [Gate Exchange Sub-Account Scenarios](references/scenarios.md)
- [Gate MCP](https://github.com/gate/gate-mcp)
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown action drafts, status tables, and result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Gate MCP authentication; write actions require explicit confirmation before execution.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact frontmatter reports 2026.3.23-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
