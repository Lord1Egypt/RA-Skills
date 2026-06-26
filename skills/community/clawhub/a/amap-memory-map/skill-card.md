## Description: <br>
Marks life memories on Amap by locating places from user stories, enriching them with map, weather, nearby-place, timeline, aggregation, and export details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[770600682-cyber](https://clawhub.ai/user/770600682-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users provide natural-language memories tied to places, and the agent turns them into structured memory cards, timelines, regional summaries, nearby-place context, and GeoJSON exports using Amap Web Service APIs. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Location queries may reveal personal places, addresses, coordinates, or travel-history details to Amap APIs. <br>
Mitigation: Avoid highly sensitive location memories unless the user is comfortable with that processing, and prefer a dedicated or limited AMAP_API_KEY. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/770600682-cyber/amap-memory-map) <br>
- [Amap Open Platform](https://lbs.amap.com) <br>
- [Amap Web Service API Documentation](https://lbs.amap.com/api/webservice/summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown responses with structured memory cards, timelines, regional summaries, and optional GeoJSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY. Location names, addresses, coordinates, and related lookup data may be sent to Amap APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
