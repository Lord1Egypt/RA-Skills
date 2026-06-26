## Description: <br>
Airport Pickups London lets agents get fixed-price UK airport and cruise port transfer quotes, validate flights, create or manage bookings, and track drivers using its MCP API with an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mfy-apl](https://clawhub.ai/user/mfy-apl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to quote, book, manage, cancel, and track UK airport and cruise port transfers through Airport Pickups London. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, amend, or cancel real airport-transfer reservations. <br>
Mitigation: Confirm the route, price, pickup time, passenger details, and requested booking action before allowing the agent to proceed. <br>
Risk: The skill shares passenger and trip details with Airport Pickups London and uses an API key for access. <br>
Mitigation: Install only when that data sharing is acceptable, provide the key only to trusted agents, and rotate or remove the key when the skill is no longer used. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mfy-apl/airport-pickups-london) <br>
- [Airport Pickups London Website](https://www.airport-pickups-london.com) <br>
- [Airport Pickups London API Key Registration](https://mcp.airport-pickups-london.com/a2a/register) <br>
- [Airport Pickups London MCP Endpoint](https://mcp.airport-pickups-london.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance, API calls] <br>
**Output Format:** [Markdown text with JSON configuration examples and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Airport Pickups London API key in the x-api-key header; booking, amendment, and cancellation actions should be confirmed by the user first.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
