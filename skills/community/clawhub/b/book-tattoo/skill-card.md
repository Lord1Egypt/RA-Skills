## Description: <br>
Book tattoo services through Lokuli's MCP server by searching providers, checking availability, and creating bookings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to ask an agent to find tattoo services, check appointment availability, and create a booking through Lokuli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A booking request may send personal contact details to Lokuli's external service. <br>
Mitigation: Confirm the customer's name, email, and phone number before submitting a booking. <br>
Risk: An incorrect provider, service, date, or time slot could create an unintended appointment. <br>
Mitigation: Confirm the provider, service, and selected time slot with the user before calling create_booking. <br>


## Reference(s): <br>
- [Book Tattoo ClawHub page](https://clawhub.ai/edwardrodriguez703-design/book-tattoo) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON-RPC MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Booking calls may include provider, service, time slot, customer name, email, and phone number.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
