## Description: <br>
Book Battery helps agents search for battery services, check availability, and create bookings through Lokuli's MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find nearby battery service options, check appointment availability, and create a booking through Lokuli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating a booking may share customer contact information with Lokuli and a service provider. <br>
Mitigation: Confirm the booking details first and provide only contact information the user is comfortable sharing. <br>
Risk: An agent could create an unwanted or incorrect appointment if provider, service, or time-slot details are not checked. <br>
Mitigation: Review provider, service, date, time, and customer details before calling the booking tool. <br>


## Reference(s): <br>
- [Book Battery ClawHub release](https://clawhub.ai/edwardrodriguez703-design/book-battery) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance] <br>
**Output Format:** [JSON-RPC MCP tool calls with concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Booking requests can include provider, service, time slot, and customer contact details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
