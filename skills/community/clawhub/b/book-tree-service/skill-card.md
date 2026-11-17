## Description:

Book Tree Service helps agents search for tree-service providers, check availability, and create bookings through Lokuli's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and booking agents use this skill to find local tree-service providers, check appointment availability, and create bookings through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad tree-service requests may be routed to an external booking service.

Mitigation: Use the skill only when the user explicitly wants tree-service provider search or booking help.

Risk: The skill can submit customer name, email, phone number, and appointment details to Lokuli.

Mitigation: Confirm user intent and get explicit approval before sharing contact or appointment details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-tree-service)
- [Publisher Profile](https://clawhub.ai/user/edwardrodriguez703-design)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown and JSON-RPC tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool-call arguments for provider search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
