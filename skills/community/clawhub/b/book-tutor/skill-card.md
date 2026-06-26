## Description: <br>
Book tutor services through Lokuli MCP. Use when user needs to find and book tutor. Triggers on requests like "book a tutor", "find tutor near me", or any tutor service request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search for tutors, check tutor availability, and create tutor-service bookings through Lokuli's MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking requests can send customer name, email, and phone number to Lokuli. <br>
Mitigation: Before creating a booking, confirm the tutor, time slot, and user consent to share contact details. <br>
Risk: The skill interacts with an external booking service. <br>
Mitigation: Install and use it only when the user intends to search for and book tutoring through Lokuli. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>
- [Book Tutor ClawHub listing](https://clawhub.ai/edwardrodriguez703-design/book-tutor) <br>
- [Publisher profile](https://clawhub.ai/user/edwardrodriguez703-design) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON-RPC MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tutor search criteria, availability checks, booking time slots, and customer contact details for Lokuli booking requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
