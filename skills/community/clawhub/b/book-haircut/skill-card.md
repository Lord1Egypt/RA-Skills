## Description:

Book haircut services through Lokuli MCP. Use when user needs to find and book haircut. Triggers on requests like "book a haircut", "find haircut near me", or any haircut service request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for haircut providers through Lokuli, check appointment availability, and create a booking with customer contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a customer's name, email, phone number, appointment choice, and provider details to Lokuli.

Mitigation: Use the skill only when the user is comfortable sharing those details with Lokuli, and show the data to be submitted before any booking action.

Risk: The skill can create a haircut booking without requiring final confirmation.

Mitigation: Require explicit user approval after presenting provider, service, time slot, and customer contact details before calling the booking tool.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-haircut)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Text or Markdown with MCP tool-call parameters and booking details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider, service, availability, customer contact, and appointment confirmation details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
