## Description: <br>
Book landscaper services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to search for landscapers, check availability, and create a landscaping service booking through Lokuli's external MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill interacts with Lokuli's external service for searches and bookings. <br>
Mitigation: Confirm booking details and user intent before invoking create_booking. <br>
Risk: Creating a booking may require sharing customer contact details with the external service. <br>
Mitigation: Only provide customer name, email, and phone number when the user intends to book. <br>


## Reference(s): <br>
- [Book Landscaper on ClawHub](https://clawhub.ai/edwardrodriguez703-design/book-landscaper) <br>
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or JSON-RPC tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Lokuli MCP search, availability, and booking tools when the user intends to book landscaping service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
