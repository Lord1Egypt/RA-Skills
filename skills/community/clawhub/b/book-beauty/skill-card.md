## Description:

Book beauty services through Lokuli MCP for haircuts, barbers, salons, nails, makeup, spa treatments, and related beauty-service requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for beauty-service providers, review pricing and availability, and create a booking after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Beauty-service search details, ZIP code, appointment choices, and booking contact information can be shared with Lokuli or a selected provider.

Mitigation: Review provider, service, time, price, and contact details before confirming a booking.

Risk: A booking could be created for the wrong provider, service, time, price, or customer contact details.

Mitigation: Require explicit user approval after presenting the full booking details and before calling create_booking.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown guidance with JSON-RPC MCP tool-call arguments and booking details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider search results, pricing, availability, user confirmation prompts, and checkout links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
