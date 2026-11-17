## Description:

Amap Memory Map helps users turn personal memories tied to places into an explorable map with geocoded memory cards, timelines, regional aggregation, current weather context, nearby point-of-interest discovery, and GeoJSON export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[770600682-cyber](https://clawhub.ai/user/770600682-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users can describe places and stories in natural language so an agent can locate them with Amap Web Service APIs, summarize them as memory cards, organize them on a timeline or by region, and export GeoJSON for sharing or visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location queries and memory details may disclose sensitive personal routines or precise places to Amap APIs.

Mitigation: Collect only the place details needed for geocoding, avoid highly sensitive memories, and make clear that place names, addresses, and coordinates are sent to Amap.

Risk: Exported GeoJSON can contain precise coordinates, dates, and story text that may expose private information if shared.

Mitigation: Review and redact GeoJSON properties and coordinate precision before saving or sharing exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/770600682-cyber/skills/amap-memory-map)
- [Amap Open Platform](https://lbs.amap.com)
- [Amap Web Service API Documentation](https://lbs.amap.com/api/webservice/summary)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Markdown summaries and JSON or GeoJSON feature collections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY; outputs may include precise coordinates, dates, place names, weather context, nearby POIs, and user story text.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
