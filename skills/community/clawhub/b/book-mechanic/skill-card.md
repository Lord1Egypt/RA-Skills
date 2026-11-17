## Description:

Book mechanic services through Lokuli MCP by searching providers, checking availability, and creating booking requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find mechanic service providers through Lokuli, check appointment availability, and request a booking after confirming service details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send personal contact details and appointment information to an external booking service.

Mitigation: Confirm the provider, service, time slot, customer name, email, and phone number before creating a booking request.

Risk: The trigger language is broader than clear booking intent for mechanic-related requests.

Mitigation: Use the booking flow only when the user intends to search for or book mechanic services through Lokuli.

## Reference(s):

- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [guidance, API calls, JSON]

**Output Format:** [Text guidance and JSON-RPC tool-call payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider, service, appointment, and customer contact details needed for a booking request.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
