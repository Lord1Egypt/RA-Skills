## Description:

Book Data Recovery helps agents search for and book data-recovery services through Lokuli's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find data-recovery services, check provider availability, and submit booking requests through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact an external booking service and send customer contact details.

Mitigation: Use it only when the user intends to search for or schedule data-recovery service, and confirm contact details before sending them.

Risk: The skill can create bookings without enough explicit scoping or consent guidance.

Mitigation: Confirm the selected provider, service, time slot, and user consent before allowing a booking request.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-data-recovery)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve external service searches, availability checks, and booking requests that include customer contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata, released 2026-02-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
