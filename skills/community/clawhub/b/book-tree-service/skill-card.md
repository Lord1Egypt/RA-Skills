## Description: <br>
Helps agents search for and book tree-service appointments through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to find tree-service providers, check appointment availability, and create bookings through Lokuli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends booking details to Lokuli as an external service provider. <br>
Mitigation: Install only if Lokuli is an acceptable provider for the deployment context. <br>
Risk: Bookings may include provider, service, time, and customer contact details. <br>
Mitigation: Confirm the provider, time, service, and contact details before creating a booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/book-tree-service) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>
- [Publisher profile](https://clawhub.ai/user/edwardrodriguez703-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-RPC MCP call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Lokuli MCP to search providers, check availability, and create bookings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
