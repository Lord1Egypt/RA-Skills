## Description:

Helps renters research supported U.S. cities and prepare a Fless apartment hunt link for their review and approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fless-io-dev](https://clawhub.ai/user/fless-io-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External renters use the skill to compare supported U.S. cities and neighborhoods, shape apartment search criteria, and prepare a prefilled hunt link. The renter reviews the link, creates the hunt, and explicitly approves any buildings before Fless contacts them.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Broad housing questions may trigger the apartment-hunting workflow, and building a hunt link transfers the housing brief to Fless before the renter creates a hunt.

Mitigation: Confirm the renter wants apartment-hunting help before collecting details, explain when their brief will be sent to Fless, and get their agreement before building the link.

## Reference(s):

- [Fless Agent Guide](https://fless.io/ai-agents)
- [Fless Hunt Guide](https://fless.io/hunt-how-to.md)
- [Fless MCP Server](https://mcp.fless.io/mcp)
- [API Reference](artifact/references/API.md)
- [City Coverage](artifact/references/CITIES.md)
- [Hunt Fields](artifact/references/HUNT_FIELDS.md)
- [Error Recovery](artifact/references/ERRORS.md)

## Skill Output:

**Output Type(s):** [Text, URLs, Guidance]

**Output Format:** [Conversational text with a prefilled hunt link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The renter creates the hunt and approves buildings in Fless before outreach begins.]

## Skill Version(s):

2.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
