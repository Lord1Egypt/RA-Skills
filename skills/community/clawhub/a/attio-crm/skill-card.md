## Description:

Manage Attio CRM records, lists, notes, tasks, and meetings through the superagnt unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to read and manage Attio CRM records, lists, attributes, notes, tasks, meetings, files, and related workspace data through a connected Attio account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence, citing workspace user and group administration beyond its stated CRM purpose and an account credits check that is not described.

Mitigation: Before installation, ask the publisher to explain these operations and confirm they are necessary and authorized; avoid invoking them until clarified.

Risk: The documented API operations include destructive CRM actions, such as deleting records and changing or overwriting data.

Mitigation: Use only endpoints needed for the user's request and confirm before deleting, overwriting, or sending on the user's behalf, as the skill directs.

## Reference(s):

- [Attio Integration documentation](https://superagnt.com/r/ch-attio-crm-docs)
- [MCP server](https://mcp.superagnt.com/mcp)
- [MCP installation instructions](https://www.superagnt.com/install)
- [ClawHub skill listing](https://clawhub.ai/superagnt/skills/attio-crm)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with curl examples and JSON API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Attio account and SUPERAGNT_API_KEY.]

## Skill Version(s):

2.0.14 (source: artifact frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
