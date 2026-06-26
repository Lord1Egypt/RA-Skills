## Description: <br>
Book Fence helps users search for fence services, check availability, and create bookings through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to search for fence service providers, check availability, and create a booking through Lokuli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating a booking may share customer name, email, phone number, and booking details with Lokuli or its service providers. <br>
Mitigation: Confirm booking details and user intent before creating a booking, and avoid collecting contact information unless the user intends to proceed. <br>
Risk: Search, availability, and booking actions depend on an external Lokuli MCP endpoint. <br>
Mitigation: Treat returned service data as live external data and ask the user to verify provider, service, time slot, and contact details before submission. <br>


## Reference(s): <br>
- [Book Fence ClawHub listing](https://clawhub.ai/edwardrodriguez703-design/book-fence) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON-RPC API calls, guidance] <br>
**Output Format:** [Text with JSON-RPC tool call arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider, service, time slot, and customer contact details when the user chooses to create a booking.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
