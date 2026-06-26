## Description: <br>
Book art-lessons services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search for art-lesson providers, check appointment availability, and request a booking through Lokuli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking requests may send customer contact details to Lokuli. <br>
Mitigation: Confirm the provider, time slot, customer name, email, and phone number with the user before creating a booking. <br>
Risk: A create_booking call may submit a real booking request. <br>
Mitigation: Ask for explicit user confirmation before sending the booking request. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/book-art-lessons) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Text] <br>
**Output Format:** [Markdown guidance with JSON-RPC MCP call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider, service, availability, time slot, and customer contact fields needed for a booking request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
