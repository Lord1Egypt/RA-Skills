## Description:

Provides AgentPMT-hosted remote tool guidance for looking up point elevations, sampling path elevations, generating elevation profile charts, and returning elevation statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call AgentPMT elevation tools for hiking, cycling, surveying, terrain analysis, real estate site evaluation, and route planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exact coordinates, paths, and chart requests are sent to AgentPMT.

Mitigation: Send only the minimum location data needed for the task and avoid including sensitive locations unless the user has approved that disclosure.

Risk: Generated chart links may be stored for seven days and exposed through signed URLs.

Mitigation: Share chart URLs only with intended recipients and avoid generating charts for sensitive routes when a numeric response is sufficient.

Risk: Unpinned npx setup commands can execute package code from the network.

Mitigation: Prefer ClawHub or OpenClaw installation routes, or verify the package source and version before running setup commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/elevation-data-point-path-charts-statistics)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/elevation-data-point-path-charts-statistics)
- [Generated Action Schema](schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON request examples and remote API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return elevation values, path statistics, and signed PNG chart URLs that expire after 7 days.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
