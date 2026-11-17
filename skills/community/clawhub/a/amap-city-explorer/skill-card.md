## Description:

Amap City Explorer generates structured city exploration guides with administrative districts, live weather, commercial areas, food, attractions, transit hubs, and POI density analysis from Amap Web Service API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[770600682-cyber](https://clawhub.ai/user/770600682-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users, travelers, and business travelers use this skill to explore a city before a trip, compare neighborhoods or cities, and receive a concise guide based on Amap map, weather, POI, and transit data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City names and query coordinates may be sent to Amap together with the configured API key.

Mitigation: Use an API key intended for this purpose and invoke the skill only when a city exploration guide is needed.

Risk: Travel, weather, POI, pricing, and popularity details can change or be incomplete in the external data source.

Mitigation: Review important recommendations against current local sources before relying on them for travel or business decisions.

## Reference(s):

- [Amap Open Platform](https://lbs.amap.com)
- [Amap Web Service API Documentation](https://lbs.amap.com/api/webservice/summary)
- [ClawHub Skill Page](https://clawhub.ai/770600682-cyber/skills/amap-city-explorer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown city guide with sections, ranked lists, tables, and comparison summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY; generated results depend on Amap Web Service API availability and returned data.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
