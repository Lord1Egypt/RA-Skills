## Description:

Access user-consented Fulcra context data including biometrics, sleep, activity, calendar, location, and the Fulcra metric catalog through the hosted MCP server or Fulcra CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to private, user-approved Fulcra context for bounded health, activity, sleep, calendar, location, and metric-catalog reads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Fulcra records, calendar details, location data, or auth material could be exposed in shared or public contexts.

Mitigation: Use the skill only for private, user-approved reads; keep requests narrowly scoped; never print tokens or raw private records; and require explicit approval before sharing or retaining outputs.

Risk: Unpinned external CLI or MCP packages could change behavior between runs.

Mitigation: Prefer pinned, reviewed versions of `fulcra-api`, `fulcra-context-mcp`, and `mcp-remote`, or use preinstalled trusted tooling before granting access to private data.

Risk: Broad exports or persistent files could retain private health, calendar, location, or file data beyond the user's intended session.

Mitigation: Confirm the exact destination and retention plan before writing local files, creating screenshots, generating charts, or exporting Fulcra data.

## Reference(s):

- [Fulcra Platform](https://fulcradynamics.com)
- [Fulcra Developer Docs](https://docs.fulcradynamics.com)
- [Fulcra Python Client](https://github.com/fulcradynamics/fulcra-api-python)
- [Fulcra Context MCP Server](https://github.com/fulcradynamics/fulcra-context-mcp)
- [Hosted Fulcra MCP Endpoint](https://mcp.fulcradynamics.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bounded read-workflow guidance; it does not ship executable helper scripts in the ClawHub package.]

## Skill Version(s):

1.4.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
