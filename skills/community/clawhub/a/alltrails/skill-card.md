## Description:

This skill should be used when the user asks about AllTrails hiking/trail data. Triggers on phrases like "find trails near", "AllTrails", "trail details", "hike reviews", "trail conditions", "my saved trails", "trails I've completed", or any request involving hiking trails, trail search, reviews, photos, or a user's AllTrails lists and activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask the agent to find trails, read trail details and reviews, check weather, or review their AllTrails lists and hiking activity. Developers can use the skill's read-only tools to retrieve this information through an authenticated browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A signed-in browser session can provide access to personal profile, saved-list, and activity data.

Mitigation: Use only with a trusted agent, review requested data and capabilities before pairing, and revoke pairing when finished.

Risk: The service integration may become unreliable, and automated use may conflict with AllTrails terms.

Mitigation: Review and pin the server version, verify the browser extension release, and check requested domains and capabilities before pairing.

## Reference(s):

- [AllTrails MCP package](https://www.npmjs.com/package/alltrails-mcp)
- [Project source linked in skill documentation](https://github.com/chrischall/alltrails-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, JSON, GPX files]

**Output Format:** [Trail and account data, summaries, and GPX 1.1 route documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only results; account-specific information requires a signed-in AllTrails browser session.]

## Skill Version(s):

3.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
