## Description: <br>
Generates Amap-backed city exploration guides with administrative areas, weather, commercial districts, food landmarks, attractions, transit hubs, and POI density analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[770600682-cyber](https://clawhub.ai/user/770600682-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, business visitors, and city researchers use this skill to quickly understand a city, compare districts or cities, and produce structured trip-planning or scouting guidance from Amap data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Amap API key and may consume quota during normal city, weather, and POI lookups. <br>
Mitigation: Use a dedicated or restricted AMAP_API_KEY where possible and monitor quota usage. <br>
Risk: City names, coordinates, and POI query terms are sent to Amap as part of normal operation. <br>
Mitigation: Avoid entering sensitive personal locations or private itinerary details when using the skill. <br>
Risk: Recommendations depend on third-party Amap data and may be incomplete, outdated, or unsuitable for a specific trip. <br>
Mitigation: Review important travel, weather, venue, pricing, and transit details against current authoritative sources before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/770600682-cyber/amap-city-explorer) <br>
- [Amap Open Platform](https://lbs.amap.com) <br>
- [Amap Web Service API documentation](https://lbs.amap.com/api/webservice/summary) <br>
- [Amap Web Service API endpoint](https://restapi.amap.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown city guide with structured sections, tables, rankings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AMAP_API_KEY-backed Amap Web Service queries for city, weather, POI, food, attraction, and transit information.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
