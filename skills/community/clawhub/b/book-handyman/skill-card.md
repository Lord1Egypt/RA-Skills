## Description: <br>
Book handyman services through Lokuli MCP. Use when user needs to find and book handyman. Triggers on requests like "book a handyman", "find handyman near me", or any handyman service request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can ask an agent to search for handyman services, check appointment availability, and create a Lokuli booking after confirming provider, service, time, and contact details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A booking could be created with the wrong provider, service, appointment time, or customer contact details. <br>
Mitigation: Confirm the provider, service, appointment time, and exact contact details before creating a booking. <br>
Risk: Customer name, email, and phone number may be sent to Lokuli during booking. <br>
Mitigation: Collect and send only the contact details required for the requested booking. <br>


## Reference(s): <br>
- [Book Handyman ClawHub Page](https://clawhub.ai/edwardrodriguez703-design/book-handyman) <br>
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Guidance] <br>
**Output Format:** [Markdown or JSON-RPC tool-call arguments, depending on the agent workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider, service, appointment, and customer contact details needed for booking.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
