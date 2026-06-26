## Description: <br>
Book Fitness helps users find and book fitness services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search for fitness services, check provider availability, and create bookings through Lokuli's MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking requests may send user contact details to Lokuli's external service. <br>
Mitigation: Ask the user to confirm their name, email, phone number, provider, service, and time before submitting a booking. <br>
Risk: Users may mistake Lokuli availability or provider information for an NVIDIA-operated service. <br>
Mitigation: Make clear that the skill uses Lokuli as a third-party booking provider. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>
- [Book Fitness ClawHub listing](https://clawhub.ai/edwardrodriguez703-design/book-fitness) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration] <br>
**Output Format:** [Markdown with JSON-RPC request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request booking details and contact information before creating a booking.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
