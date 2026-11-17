## Description:

Access Coupler.io data flows configured with an OpenClaw destination to list flows, inspect schemas, and query data through an OAuth-secured read-only MCP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nika-is-nika](https://clawhub.ai/user/nika-is-nika)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to connect to Coupler.io's MCP server, authenticate with OAuth, discover available OpenClaw-destination dataflows, inspect schemas, and run read-only SQL queries over flow data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected Coupler.io account may expose dataflows through the OpenClaw destination.

Mitigation: Install only when that account access is intended, and review which Coupler dataflows are exposed before use.

Risk: Persisted mcporter OAuth configuration represents sensitive account access material.

Mitigation: Store the mcporter configuration securely and reset or re-authenticate credentials when access should be refreshed.

## Reference(s):

- [Coupler.io](https://coupler.io)
- [mcporter CLI](https://github.com/openclaw/mcporter)
- [ClawHub Skill Page](https://clawhub.ai/nika-is-nika/skills/coupler-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only MCP usage guidance for OAuth setup, dataflow discovery, schema inspection, and SQL query calls.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
