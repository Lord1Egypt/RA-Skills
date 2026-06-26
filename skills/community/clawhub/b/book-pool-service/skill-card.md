## Description: <br>
Book Pool Service helps agents search for pool service providers, check availability, and create bookings through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find pool service options, check provider availability, and create a booking when the user intends to request pool service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating a booking sends customer contact information to Lokuli for the service request. <br>
Mitigation: Use booking actions only when the user intends to book pool service, and confirm provider, time slot, and contact details before creating the booking. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/book-pool-service) <br>
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON-RPC MCP call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May collect and send customer contact details to Lokuli when creating a booking.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
