## Description: <br>
Book Nutritionist helps agents find nutritionists and create bookings through Lokuli's MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search for nutritionist services, check appointment availability, and create a booking through Lokuli after confirming the provider, time slot, and contact details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating a booking sends the user's name, email, and phone number to Lokuli. <br>
Mitigation: Confirm the provider, appointment time, and consent to share contact details before creating the booking. <br>
Risk: The skill relies on Lokuli as the external booking service. <br>
Mitigation: Install and use the skill only when the user is comfortable using Lokuli for nutritionist booking. <br>


## Reference(s): <br>
- [Book Nutritionist on ClawHub](https://clawhub.ai/edwardrodriguez703-design/book-nutritionist) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance] <br>
**Output Format:** [JSON-RPC MCP tool calls and text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Lokuli search, availability, and booking tools with user-provided appointment and contact details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
