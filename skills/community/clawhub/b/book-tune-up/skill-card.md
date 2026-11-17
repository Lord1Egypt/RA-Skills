## Description:

Book tune-up services through Lokuli MCP. Use when user needs to find and book tune-up. Triggers on requests like "book a tune-up", "find tune-up near me", or any tune-up service request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to search for tune-up services through Lokuli, check provider availability, and prepare a booking request. It is intended for service discovery and booking workflows where the user confirms provider, service, time, and contact details before a reservation is submitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send personal contact details to an external booking service.

Mitigation: Only provide contact details when the user intends to create a booking and has confirmed the data sharing.

Risk: The skill can create reservations without explicit consent or confirmation instructions in the source.

Mitigation: Confirm provider, service, time slot, customer details, and booking intent before submitting any reservation.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external MCP service for tune-up search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
