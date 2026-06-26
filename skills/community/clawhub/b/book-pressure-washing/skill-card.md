## Description: <br>
Book pressure-washing services through Lokuli MCP for users who need to find providers, check availability, and create a booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search for pressure-washing services near a ZIP code, check provider availability, and create a booking through Lokuli's MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking actions may share customer contact details or create a service booking. <br>
Mitigation: Before using create_booking, confirm the provider, service, date and time, available cost or terms, and exact contact details that will be sent to Lokuli. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance] <br>
**Output Format:** [Markdown with JSON-RPC tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may guide calls that send provider, service, appointment, and customer contact details to Lokuli.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
