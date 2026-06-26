## Description: <br>
Amap Smart Route helps an agent plan driving, walking, transit, and bicycling routes with estimated duration, distance, route options, and Amap navigation links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[770600682-cyber](https://clawhub.ai/user/770600682-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for route planning between named places, compare transportation modes, and receive distances, estimated durations, and navigation links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route requests share start and destination addresses or coordinates with Amap. <br>
Mitigation: Avoid highly sensitive locations and disclose that route inputs are sent to Amap for calculation. <br>
Risk: The skill requires an Amap API key that may have quota or billing impact. <br>
Mitigation: Use a dedicated AMAP_API_KEY with appropriate limits and monitor usage. <br>
Risk: The publisher is a third-party ClawHub user, not server-proven to be Amap or NVIDIA. <br>
Mitigation: Verify the publisher before relying on this as an official Amap-provided skill. <br>


## Reference(s): <br>
- [Amap Open Platform](https://lbs.amap.com) <br>
- [Amap Web Service API Summary](https://lbs.amap.com/api/webservice/summary) <br>
- [Amap Geocoding API Documentation](https://lbs.amap.com/api/webservice/guide/api/georegeo) <br>
- [Amap Route Planning API Documentation](https://lbs.amap.com/api/webservice/guide/api/newroute) <br>
- [Amap Smart Route on ClawHub](https://clawhub.ai/770600682-cyber/amap-smart-route) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown route-planning guidance with route metrics and navigation links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY and sends route start and destination addresses or coordinates to Amap for route calculation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
