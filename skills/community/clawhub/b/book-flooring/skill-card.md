## Description: <br>
Book flooring services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find flooring providers through Lokuli, check availability, and create a booking through the Lokuli MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send customer contact details to an external booking provider. <br>
Mitigation: Install only if using Lokuli as the external provider is acceptable, and require the agent to show the name, email, and phone number before submission. <br>
Risk: The skill can create a real flooring-service booking without clear confirmation safeguards in the artifact. <br>
Mitigation: Require explicit user approval after showing the provider, service, date, and time before allowing the booking request. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown with JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Lokuli MCP over SSE and JSON-RPC to search for flooring services, check availability, and create bookings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
