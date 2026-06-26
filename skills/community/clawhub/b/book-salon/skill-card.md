## Description: <br>
Book salon services through Lokuli MCP. Use when user needs to find and book salon. Triggers on requests like "book a salon", "find salon near me", or any salon service request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to search for salon services, check appointment availability, and create a salon booking through Lokuli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bookings may send a user's name, email, phone number, selected service, and appointment time to Lokuli. <br>
Mitigation: Confirm the salon, service, appointment time, and exact contact details with the user before creating a booking. <br>
Risk: The skill can create real salon appointments through the external booking flow. <br>
Mitigation: Require explicit user confirmation before calling the booking action. <br>


## Reference(s): <br>
- [Book Salon on ClawHub](https://clawhub.ai/edwardrodriguez703-design/book-salon) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [Markdown and JSON-RPC tool call arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include salon search criteria, availability details, and booking contact details supplied by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
