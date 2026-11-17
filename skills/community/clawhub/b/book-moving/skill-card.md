## Description:

Book moving services through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can ask an agent to search for moving providers, check availability, and book a moving service through Lokuli's MCP service. The agent should confirm before sending contact details or booking selections to the external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send personal contact details, ZIP code, moving date, and booking choices to an external booking service.

Mitigation: Ask for explicit user confirmation before sending name, email, phone number, ZIP code, date, or booking selections to the Lokuli MCP service.

Risk: The security verdict is suspicious because consent and privacy instructions are not clear in the artifact.

Mitigation: Review before installing and use the skill only when the user intentionally wants to search or book moving services through Lokuli.

## Reference(s):

- [Book Moving on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-moving)
- [Publisher profile](https://clawhub.ai/user/edwardrodriguez703-design)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown with JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool-call guidance for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
