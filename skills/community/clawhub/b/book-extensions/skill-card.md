## Description:

Book extensions services through Lokuli MCP. Use when user needs to find and book extensions. Triggers on requests like "book a extensions", "find extensions near me", or any extensions service request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for extensions services through Lokuli, check provider availability, and request a booking when the user has chosen a provider and time slot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create appointments using personal contact details without clear consent or confirmation guidance.

Mitigation: Confirm the provider, service, time slot, customer name, email, and phone number before allowing a booking request to be sent.

Risk: The skill contacts a third-party Lokuli service to search and book extensions services.

Mitigation: Use this skill only when the user explicitly asks for booking help through Lokuli.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-extensions)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown guidance with JSON-RPC tool call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service search criteria, provider availability, selected booking time, and customer contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
