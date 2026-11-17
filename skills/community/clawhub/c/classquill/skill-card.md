## Description:

Query a ClassQuill tutoring business -- sessions, students, tutors, parents, invoices, payments, lesson plans, bookings, earnings, and reports -- through the ClassQuill MCP server / public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandoncollis](https://clawhub.ai/user/brandoncollis)

### License/Terms of Use:

MIT-0

## Use Case:

Tutoring business operators, administrators, and support agents use this skill to answer questions about live ClassQuill operations, scheduling, billing, students, tutors, and reports. It supports read-only, organization-scoped access through the user's ClassQuill credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a live ClassQuill API key that may grant read access to organization data.

Mitigation: Use OAuth or protected secret storage when available, avoid pasting live keys into chat, and rotate any key that is shared accidentally.

Risk: The local setup path can run an unpinned npm MCP server that receives the API key.

Mitigation: Prefer the hosted MCP server or pin and review the npm package version before running it in a restricted environment.

## Reference(s):

- [Hosted ClassQuill MCP Server](https://mcp.classquill.com/mcp)
- [ClassQuill Public API](https://api.classquill.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown with optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only responses based on live, organization-scoped ClassQuill data when the MCP server or API is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
