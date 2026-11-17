## Description:

Amap Search Skill helps agents use the Gaode/AMap Web Service APIs for POI search, geocoding, reverse geocoding, route planning, weather, traffic, IP location, and input tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahongting](https://clawhub.ai/user/mahongting)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to query Chinese map and location data, plan routes, check weather and traffic, and format Gaode/AMap results for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map queries, addresses, coordinates, route endpoints, and IP-derived location data are sent to Gaode/AMap.

Mitigation: Use the skill only with location data appropriate for that service and avoid sensitive locations unless the user's privacy requirements allow it.

Risk: Supplying API keys on the command line can expose them through shell history, process listings, or logs.

Mitigation: Prefer AMAP_API_KEY from a secure environment or secret store, restrict the key in the Gaode console where possible, and rotate it if exposed.

Risk: Route, weather, POI, and traffic results depend on a third-party API and may be unavailable, rate-limited, stale, or inaccurate.

Mitigation: Handle API errors and confirm critical travel, routing, or location decisions with authoritative sources before acting.

## Reference(s):

- [Gaode Open Platform](https://lbs.amap.com/)
- [ClawHub skill page](https://clawhub.ai/mahongting/skills/amap-search-skill)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON command output, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Gaode/AMap Web Service API key via AMAP_API_KEY or --key.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
