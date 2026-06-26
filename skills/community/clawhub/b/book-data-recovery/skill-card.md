## Description: <br>
Book Data Recovery helps users find and book data-recovery services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search for data-recovery providers, check availability, and create bookings through Lokuli after confirming service and contact details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send contact details to an external booking service when creating a booking. <br>
Mitigation: Confirm the provider, service, time slot, name, email, and phone number before creating a booking, and do not share contact details unless the user intends them to be sent. <br>
Risk: Booking through Lokuli depends on an external MCP endpoint and provider availability. <br>
Mitigation: Use the search and availability tools before booking, and clearly present available providers and time slots for user confirmation. <br>


## Reference(s): <br>
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse) <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/book-data-recovery) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON-RPC tool calls with concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Lokuli MCP search, availability, and booking tools; booking requests may include customer name, email, and phone number.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
