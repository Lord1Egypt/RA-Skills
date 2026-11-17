## Description:

Query and manage GPS travel data from Geomanic — your privacy-first GPS tracking platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weltspion](https://clawhub.ai/user/weltspion)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect OpenClaw to Geomanic so an agent can query travel statistics, list or retrieve waypoints, and create, update, or delete GPS waypoint records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive GPS history and travel patterns.

Mitigation: Install it only for users who intend to grant OpenClaw access to their Geomanic travel data, and avoid sharing raw location results unnecessarily.

Risk: The skill can create, update, or delete GPS waypoint records.

Mitigation: Confirm the exact waypoint and intended change before running create, update, or delete actions.

Risk: GEOMANIC_TOKEN grants authenticated access to Geomanic data.

Mitigation: Treat GEOMANIC_TOKEN like a password and keep it in local secret storage or environment configuration.

## Reference(s):

- [Geomanic](https://geomanic.com)
- [Geomanic API endpoint](https://geomanic.com/api/v1/mcp)
- [Geomanic data and API key settings](https://geomanic.com/data)
- [Geomanic MCP Bridge](https://github.com/monswyk/geomanic-mcp)
- [ClawHub skill page](https://clawhub.ai/weltspion/skills/geomanic)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON-RPC curl examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEOMANIC_TOKEN for authenticated Geomanic API requests.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
