## Description:

Book Laundry helps an agent find laundry services, check availability, and create bookings through Lokuli's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can ask an agent to search for nearby laundry providers, check availability, and create a booking through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send customer contact details to Lokuli.

Mitigation: Use it only when the user agrees to share booking contact details with Lokuli.

Risk: The skill can create laundry bookings without explicit confirmation guidance in the artifact.

Mitigation: Confirm the provider, time slot, and personal information with the user before creating a booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-laundry)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [guidance, API calls]

**Output Format:** [Text with JSON-RPC tool call payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include search results, availability checks, and booking requests that contain customer contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
