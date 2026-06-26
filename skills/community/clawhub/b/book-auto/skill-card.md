## Description: <br>
Book Auto helps agents search, present, check availability for, and book automotive services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find auto-service providers, compare pricing and available time slots, and create a booking after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may share booking details such as customer name, email, phone number, preferred time, provider, service, and location with Lokuli. <br>
Mitigation: Before creating a booking, review the provider, service, price, time slot, and contact details with the user and obtain explicit approval. <br>
Risk: Search results, prices, or availability may be stale, incomplete, or unsuitable for the user's vehicle or location. <br>
Mitigation: Present options clearly, confirm the selected provider and service details, and use availability checks before generating a checkout link. <br>


## Reference(s): <br>
- [Book Auto on ClawHub](https://clawhub.ai/edwardrodriguez703-design/book-auto) <br>
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Markdown summaries with JSON-RPC tool call arguments and booking guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider options, prices, availability, checkout links, and customer contact details needed for booking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
