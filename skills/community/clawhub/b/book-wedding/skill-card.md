## Description: <br>
Book Wedding helps agents search for wedding services, check availability, and create bookings through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to find wedding-service providers, check service availability, and create bookings after confirming the provider, service, schedule, cost, terms, and contact details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send customer contact details to an external wedding-service platform. <br>
Mitigation: Require explicit user confirmation of the exact name, email, phone number, provider, service, date, and time before sending booking details to Lokuli. <br>
Risk: The skill can create real bookings without clear confirmation safeguards in the artifact. <br>
Mitigation: Require the agent to confirm cost or deposit, cancellation terms, provider identity, service identity, and selected time slot before calling the booking tool. <br>


## Reference(s): <br>
- [Book Wedding ClawHub listing](https://clawhub.ai/edwardrodriguez703-design/book-wedding) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, JSON] <br>
**Output Format:** [Markdown with JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Lokuli MCP tools for search, availability checks, and booking creation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
