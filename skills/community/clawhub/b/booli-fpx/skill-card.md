## Description:

Query Booli's Swedish property listings and property details from the shell using fpx and a paired browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use the skill in shell workflows to resolve Booli areas, search current and sold property listings, and retrieve property details through Booli's GraphQL endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external fpx CLI and ContextMint Bridge extension releases were not fully audited.

Mitigation: Review the CLI and extension before installing; approve only booli.se with fetch capability.

Risk: Browser pairing persists after approval.

Mitigation: Use a signed-out tab for public queries and revoke pairing through the extension popup when finished, following the bridge's revocation instructions.

## Reference(s):

- [Booli GraphQL query examples](references/graphql-queries.md)
- [Booli GraphQL endpoint](https://www.booli.se/graphql)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge pairing revocation guidance](https://github.com/nullnet-app/contextmint-bridge/blob/main/docs/PRIVACY.md#6-revoking-access)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [GraphQL query examples and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include property listing, sale, and detail fields in Booli's GraphQL JSON format.]

## Skill Version(s):

2.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
