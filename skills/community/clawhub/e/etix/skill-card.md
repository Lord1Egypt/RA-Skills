## Description:

Search Etix events, venues, and performers and retrieve event or venue details through MCP, with etix-mcp and an active ContextMint Bridge extension connected to an open etix.com tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to find Etix events, performers, and venues, then retrieve event or venue details through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests use the active Etix browser session through a paired extension; the external package and extension binaries were not audited in this review.

Mitigation: Review and pin the npm package version, verify the extension download, and check pairing permissions before approving.

## Reference(s):

- [Etix](https://www.etix.com/ticket/)
- [etix-mcp package](https://www.npmjs.com/package/etix-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Event, venue, and performer search results and details, including dates, locations, and price information when available.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
