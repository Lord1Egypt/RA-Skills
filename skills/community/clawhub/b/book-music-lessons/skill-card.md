## Description:

Book music lessons through Lokuli by searching providers, checking availability, and creating bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill with an agent to find music-lesson providers through Lokuli, check availability, and create a booking after confirming provider, time, and contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a booking sends the user's name, email, and phone number to an external booking service.

Mitigation: Before booking, confirm the provider, time slot, and contact details, and make clear that the contact details will be sent to Lokuli.

Risk: The skill can create real booking requests through an external service.

Mitigation: Ask for explicit user confirmation before calling the booking tool.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-music-lessons)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown and JSON-RPC tool-call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate search, availability, and booking requests to Lokuli MCP using user-provided location and contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
