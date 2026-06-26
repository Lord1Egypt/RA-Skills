## Description: <br>
Book car-wash services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search for car-wash services, check availability, and create a booking through Lokuli's MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Lokuli as an external third-party booking service and may submit personal contact details when creating a booking. <br>
Mitigation: Install only if the user is comfortable using Lokuli, and confirm the name, email, phone number, provider, service, time slot, price, and cancellation terms before creating a booking. <br>
Risk: A booking may be created for the wrong provider, service, date, or time if availability details are not reviewed. <br>
Mitigation: Review the selected provider, service, and time slot with the user before calling the create_booking tool. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>
- [ClawHub skill listing](https://clawhub.ai/edwardrodriguez703-design/book-car-wash) <br>
- [Publisher profile](https://clawhub.ai/user/edwardrodriguez703-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or structured JSON-RPC tool-call arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May collect and submit booking details such as name, email, phone number, provider, service, and time slot.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
