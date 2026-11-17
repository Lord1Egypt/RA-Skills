## Description:

Helps renters research supported cities, collect apartment preferences, and create a pre-filled Fless hunt link for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fless-io-dev](https://clawhub.ai/user/fless-io-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Renters and their assistants use this skill to check Fless city coverage, compare neighborhoods, gather search criteria, and prepare a hunt link. The renter reviews matched buildings and approves any outreach.

### Deployment Geography for Use:

United States (currently supported cities in Florida, Georgia, Maryland, and Virginia; check live coverage before starting a hunt)

## Known Risks and Mitigations:

Risk: Broad apartment or neighborhood questions may activate the skill and share search criteria with Fless when building a hunt link.

Mitigation: Use the skill only for an intentional Fless-assisted hunt; review the criteria and generated link before opening it.

Risk: City coverage and matched-building details may not meet the renter's needs.

Mitigation: Check live city coverage and research results, then let the renter review matched buildings and explicitly approve outreach.

## Reference(s):

- [Fless agent overview](https://fless.io/ai-agents)
- [Fless hunt guide](https://fless.io/hunt-how-to.md)
- [Fless MCP server](https://mcp.fless.io/mcp)
- [API reference](references/API.md)
- [City coverage](references/CITIES.md)
- [Hunt fields](references/HUNT_FIELDS.md)
- [Error recovery](references/ERRORS.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Links]

**Output Format:** [Markdown with a pre-filled hunt link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The renter confirms the hunt and approves matched buildings before Fless contacts them.]

## Skill Version(s):

2.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
