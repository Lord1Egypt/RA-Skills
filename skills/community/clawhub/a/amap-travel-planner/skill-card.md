## Description:

Amap Travel Planner helps agents build travel itineraries with Amap route data for destinations, schedules, budgets, checklists, food search, route optimization, and map QR code output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[770600682-cyber](https://clawhub.ai/user/770600682-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to plan China-focused trips with Amap-backed travel times, distances, transportation choices, budget estimates, route ordering, and scannable Amap maps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel addresses, points of interest, route queries, and generated map data are sent to Amap services using the configured API key.

Mitigation: Avoid entering sensitive private locations unless the user accepts sharing that data with Amap; configure and protect AMAP_API_KEY as a credential.

Risk: Route, time, distance, fee, and POI recommendations may be incomplete or stale because they depend on Amap service responses.

Mitigation: Review final itineraries before booking or travel, and verify critical routes, operating hours, and costs with authoritative local sources.

## Reference(s):

- [Amap Open Platform](https://lbs.amap.com)
- [Amap Web Service API Documentation](https://lbs.amap.com/api/webservice/summary)
- [Amap Web Service API Endpoint](https://restapi.amap.com)
- [ClawHub skill page](https://clawhub.ai/770600682-cyber/skills/amap-travel-planner)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown travel plan with route data, budget tables, checklist guidance, and Amap map QR code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY and sends travel locations, POIs, routes, and generated map data to Amap services.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
