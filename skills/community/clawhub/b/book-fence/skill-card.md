## Description:

Book Fence helps agents find fence services and book appointments through Lokuli's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users or agents use this skill to search for fence service providers, check appointment availability, and create bookings through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send customer contact details to an external booking service.

Mitigation: Require the agent to show the provider, time slot, customer name, email, and phone number and get explicit confirmation before creating a booking.

Risk: The skill performs transactional booking actions through Lokuli.

Mitigation: Use it only when the user intends to contact or book a fence service, and confirm the booking target and appointment details before submission.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [Book Fence on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-fence)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-RPC request bodies for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
