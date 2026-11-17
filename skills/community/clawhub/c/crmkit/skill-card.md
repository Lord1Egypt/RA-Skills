## Description:

An agent-first CRM, built for an AI agent to operate over a plain-text HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pdparchitect](https://clawhub.ai/user/pdparchitect)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and CRM operators use this skill to authenticate with CRM Kit, query and update contacts, companies, deals, activities, workspaces, members, tokens, reminders, and audit logs through HTTP or MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad read and write authority over CRM records in the selected workspace.

Mitigation: Install only for trusted crmkit.ai workspaces, scope tokens to the intended workspace, confirm destructive or sensitive actions with the user, and review audit logs when available.

Risk: The skill relies on bearer tokens that may be long-lived when used regularly.

Mitigation: Store tokens only in a secure credential manager, avoid putting tokens in chat memory or transcripts, and review or revoke active tokens with the documented token endpoints.

## Reference(s):

- [CRM Kit ClawHub Page](https://clawhub.ai/pdparchitect/skills/crmkit)
- [CRM Kit API Base URL](https://api.crmkit.ai)
- [CRM Kit MCP Endpoint](https://api.crmkit.ai/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown operating manual with HTTP endpoint examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses from the CRM service are plain text by default or JSON when requested.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
