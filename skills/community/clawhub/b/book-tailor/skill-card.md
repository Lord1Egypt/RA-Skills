## Description:

Book Tailor helps agents search for and book tailor services through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to find tailor providers, check availability, and create bookings through Lokuli. Users should confirm the provider, time slot, and contact details before allowing a booking request to be sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create external bookings and send contact details to Lokuli without an explicit confirmation or privacy step.

Mitigation: Confirm the provider, time slot, and contact details with the user before allowing any booking request to be sent.

Risk: The security evidence recommends review before installation and reports a suspicious verdict.

Mitigation: Review the skill before installing and use it only when the user intends to search for or book tailor services through Lokuli.

## Reference(s):

- [Book Tailor on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-tailor)
- [Lokuli MCP SSE endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown instructions with JSON-RPC tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SSE transport to call Lokuli MCP tools for search, availability, and booking.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
