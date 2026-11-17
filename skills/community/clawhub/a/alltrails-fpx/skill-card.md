## Description:

Query AllTrails trail and account data from a shell using fpx through a signed-in browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use shell commands to search AllTrails and retrieve trail details, reviews, photos, weather, route data, and account activity through an already signed-in browser tab.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A signed-in browser tab can expose the AllTrails account information available through that session.

Mitigation: Use an account whose available data the agent is permitted to read, and limit browser site access and header capture to the documented AllTrails domain and header.

Risk: Fixed temporary files may retain API output despite the documentation's no-storage claim.

Mitigation: Use private, uniquely created temporary files and delete them after use.

## Reference(s):

- [AllTrails endpoints for fpx](references/endpoints.md)
- [AllTrails](https://www.alltrails.com)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only AllTrails data; distance and elevation values are returned in meters.]

## Skill Version(s):

3.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
