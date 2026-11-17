## Description:

Book UK airport and cruise port transfers via Airport Pickups London. Get instant fixed-price quotes, validate flights, create bookings, amend, cancel, and track drivers live. TfL-licensed, 24/7 service. Requires API key (free instant registration).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfy-apl](https://clawhub.ai/user/mfy-apl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel operations agents use this skill to quote, book, amend, cancel, and track UK airport and cruise port transfers through Airport Pickups London's service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent connects to Airport Pickups London's remote MCP/API service and may send passenger contact details, trip locations, and flight numbers.

Mitigation: Install only after confirming the data-sharing posture is acceptable, and provide only the passenger and trip details needed for the transfer.

Risk: The skill can create, amend, or cancel live transfer bookings.

Mitigation: Require explicit user confirmation before any booking, amendment, or cancellation action.

Risk: The skill requires an API key for the remote service.

Mitigation: Keep the API key in the MCP client configuration or a secrets store and do not expose it in prompts, logs, or shared transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mfy-apl/skills/airport-pickups-london)
- [Publisher profile](https://clawhub.ai/user/mfy-apl)
- [Airport Pickups London homepage](https://www.airport-pickups-london.com)
- [Airport Pickups London MCP registration endpoint](https://mcp.airport-pickups-london.com/a2a/register)
- [Airport Pickups London MCP server](https://mcp.airport-pickups-london.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and shell command examples, plus MCP tool responses from the remote service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and explicit user confirmation before booking, amendment, or cancellation actions.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
