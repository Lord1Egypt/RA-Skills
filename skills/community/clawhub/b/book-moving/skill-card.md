## Description: <br>
Book Moving helps an agent search for moving providers, check availability, and create bookings through Lokuli's MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People planning a move can use this skill through an agent to find moving services near a ZIP code, check provider availability, and prepare a booking after confirming the provider, time, price, cancellation terms, and contact details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit personal contact details and booking details to Lokuli and connected moving providers. <br>
Mitigation: Confirm the provider, appointment time, price, cancellation terms, and the user's consent to share name, email, phone number, and booking details before creating a booking. <br>
Risk: Availability, pricing, and cancellation terms may depend on external providers returned by the Lokuli MCP endpoint. <br>
Mitigation: Use the skill to check availability and present provider-specific terms to the user before treating a booking as final. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/book-moving) <br>
- [Publisher profile](https://clawhub.ai/user/edwardrodriguez703-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON-RPC API calls, guidance] <br>
**Output Format:** [Plain text or Markdown with JSON-RPC request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before submitting booking details to Lokuli or connected providers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
