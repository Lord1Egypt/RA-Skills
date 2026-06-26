## Description: <br>
Book blowout services through Lokuli MCP. Use when user needs to find and book blowout. Triggers on requests like "book a blowout", "find blowout near me", or any blowout service request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find blowout services, check provider availability, and create bookings through Lokuli's MCP server. It is intended for appointment booking workflows that may require location, selected provider and service, appointment time, and customer contact details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send personal contact details and booking selections to an external booking service. <br>
Mitigation: Require explicit user approval before sending name, email, phone number, location or ZIP code, selected provider, service, appointment time, and final booking terms. <br>
Risk: The skill can create a real appointment through the external service. <br>
Mitigation: Confirm the appointment details and user consent immediately before invoking the booking creation tool. <br>


## Reference(s): <br>
- [ClawHub listing for Book Blowout](https://clawhub.ai/edwardrodriguez703-design/book-blowout) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown with JSON-RPC request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can guide calls to Lokuli MCP tools for search, availability checks, and booking creation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
