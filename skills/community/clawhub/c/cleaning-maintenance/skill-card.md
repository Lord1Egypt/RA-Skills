## Description:

Book cleanings and manage property maintenance by scheduling one-time or recurring cleanings, reporting and tracking maintenance issues, managing service professionals, and checking availability and pricing through CLI, MCP, or REST API approaches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mchusma](https://clawhub.ai/user/mchusma)

### License/Terms of Use:

MIT-0

## Use Case:

Homeowners, office managers, and building managers use this skill to ask an agent to book cleanings, manage recurring schedules, report maintenance issues, track status, and coordinate service professionals through TIDY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real-world property-service actions such as booking, canceling, deleting, spending, or assigning concierge work.

Mitigation: Require explicit human confirmation before those actions are submitted.

Risk: Property addresses, access notes, booking data, maintenance details, and vendor contact information may be shared with TIDY.

Mitigation: Use the skill only when the user trusts TIDY with that information, and do not include hidden-key locations or other entry secrets in notes.

Risk: TIDY tokens are long-lived credentials.

Mitigation: Store TIDY_API_TOKEN securely, restrict access to the runtime environment, and rotate the token if exposure is suspected.

## Reference(s):

- [TIDY Homepage](https://tidy.com)
- [Authentication](references/authentication.md)
- [Cleaning & Maintenance Workflows](references/maintenance-workflows.md)
- [MCP Server Reference](references/mcp-server-reference.md)
- [REST API Reference](references/rest-api-reference.md)
- [TIDY Public API Docs](https://public-api.tidy.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and REST API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI, MCP, and REST API paths for the same cleaning or maintenance workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
