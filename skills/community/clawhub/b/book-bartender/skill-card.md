## Description: <br>
Book bartender services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to search for bartender services, check provider availability, and create a booking through Lokuli's MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking requests may send personal contact details to a third-party Lokuli endpoint. <br>
Mitigation: Before creating a booking, show the selected provider, service, date and time, and contact details, and only proceed after the user confirms. <br>
Risk: The skill can initiate a real service booking through the disclosed MCP endpoint. <br>
Mitigation: Treat booking creation as an explicit user-confirmed action rather than an automatic follow-up to search or availability checks. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>
- [Book Bartender ClawHub page](https://clawhub.ai/edwardrodriguez703-design/book-bartender) <br>
- [Publisher profile](https://clawhub.ai/user/edwardrodriguez703-design) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Text] <br>
**Output Format:** [Markdown instructions with JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a disclosed Lokuli MCP endpoint for search, availability checks, and booking creation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
