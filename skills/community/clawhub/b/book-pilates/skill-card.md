## Description: <br>
Book Pilates helps users search for pilates services, check availability, and create bookings through Lokuli's MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can ask an agent to find nearby pilates services, check provider availability, and create a booking through Lokuli after reviewing the provider, service, time, and contact details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact an external booking service and create real reservations with personal contact details. <br>
Mitigation: Require the agent to show the provider, service, time, and contact details for explicit user approval before sending personal information or creating a reservation. <br>
Risk: The release security verdict is suspicious and recommends review before installation. <br>
Mitigation: Review the skill before installing and use it only when the user intends to search for or book pilates through Lokuli. <br>


## Reference(s): <br>
- [Book Pilates ClawHub listing](https://clawhub.ai/edwardrodriguez703-design/book-pilates) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance] <br>
**Output Format:** [Markdown with JSON-RPC request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider, service, availability, time slot, and customer contact details for booking approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
