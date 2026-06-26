## Description: <br>
Book locksmith services through Lokuli MCP. Use when user needs to find and book locksmith. Triggers on requests like "book a locksmith", "find locksmith near me", or any locksmith service request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search for locksmith providers, check appointment availability, and create a locksmith service booking through Lokuli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a real locksmith booking through a third-party service. <br>
Mitigation: Require explicit user confirmation before calling create_booking, including provider, service, time, expected cost, and cancellation terms. <br>
Risk: The booking flow can transmit personal contact details to Lokuli. <br>
Mitigation: Confirm the exact customer name, email, and phone number with the user before sending them. <br>


## Reference(s): <br>
- [Book Locksmith on ClawHub](https://clawhub.ai/edwardrodriguez703-design/book-locksmith) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May search providers, check availability, and prepare booking requests that include customer contact details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
