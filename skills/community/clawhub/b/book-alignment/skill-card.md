## Description: <br>
Book alignment services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and service-booking agents use this skill to search for alignment services, check availability, and create a booking through Lokuli's MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking requests send personal contact details to Lokuli's external service. <br>
Mitigation: Before creating a booking, review the provider, service, date, time, customer name, email, and phone number that will be sent. <br>
Risk: The selected provider, service, or time slot may be wrong if search or availability results are not reviewed. <br>
Mitigation: Confirm the provider, service, date, and time with the user before calling create_booking. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/edwardrodriguez703-design/book-alignment) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls] <br>
**Output Format:** [Markdown with JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Lokuli MCP search, availability, and booking calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
