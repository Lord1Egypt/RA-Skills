## Description: <br>
Book Towing helps agents search for towing providers, check availability, and create bookings through Lokuli's MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and service agents use this skill to find towing providers, check available appointment times, and submit towing booking details through Lokuli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking requests may share customer contact information with Lokuli's external service. <br>
Mitigation: Confirm the customer name, email, phone number, provider, service, and time slot before creating a booking. <br>
Risk: A user may book towing without understanding provider terms or costs. <br>
Mitigation: Confirm the provider, time slot, cost or cancellation terms when available, and the user's intent before booking. <br>


## Reference(s): <br>
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse) <br>
- [Book Towing on ClawHub](https://clawhub.ai/edwardrodriguez703-design/book-towing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, Guidance] <br>
**Output Format:** [JSON-RPC tool calls and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May transmit customer contact details and booking selections to Lokuli's external service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
