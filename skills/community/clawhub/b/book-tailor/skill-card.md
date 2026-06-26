## Description: <br>
Book tailor services through Lokuli MCP. Use when user needs to find and book tailor. Triggers on requests like "book a tailor", "find tailor near me", or any tailor service request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search for tailor providers, check appointment availability, and create a booking through Lokuli's MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking requests can share customer name, email, and phone number with Lokuli. <br>
Mitigation: Confirm the exact contact details before using create_booking. <br>
Risk: An incorrect provider, service, appointment time, price, or cancellation term could result in an unwanted booking. <br>
Mitigation: Confirm the provider, service, appointment time, and any available price or cancellation terms before booking. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>
- [ClawHub Book Tailor listing](https://clawhub.ai/edwardrodriguez703-design/book-tailor) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance] <br>
**Output Format:** [JSON-RPC tool calls and concise natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request or pass provider, service, appointment, and customer contact details to Lokuli.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
