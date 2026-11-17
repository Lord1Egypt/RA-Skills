## Description:

Book braids services through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to search for braid services, check appointment availability, and request bookings through Lokuli's MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create bookings and send customer contact details to an external service without sufficiently explicit consent in the artifact.

Mitigation: Invoke booking only after the user confirms the provider, service, time slot, and contact details to share.

Risk: The security review marked the release suspicious because booking scope and consent are not clearly constrained.

Mitigation: Review before installing and limit use to cases where the user intentionally wants to search or book braid services through Lokuli.

## Reference(s):

- [Book Braids ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-braids)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Text]

**Output Format:** [Text with MCP tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service search criteria, availability details, and booking contact fields.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
