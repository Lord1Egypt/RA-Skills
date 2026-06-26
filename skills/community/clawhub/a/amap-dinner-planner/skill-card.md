## Description: <br>
Amap Dinner Planner helps groups choose a dinner location by geocoding each participant's position, finding a convenient middle area, recommending nearby restaurants, comparing travel time, and producing an Amap map QR code for sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[770600682-cyber](https://clawhub.ai/user/770600682-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan group meals by turning multiple participant locations and dining preferences into ranked restaurant options, commute comparisons, and a shareable Amap map QR code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Addresses, meeting areas, and restaurant preferences may be sent to Amap services during geocoding, search, routing, and QR map generation. <br>
Mitigation: Tell users before collection, avoid highly sensitive private locations, and use only the minimum location detail needed to plan the meal. <br>
Risk: The skill requires an Amap API key, which could be exposed or over-permissioned if handled carelessly. <br>
Mitigation: Store AMAP_API_KEY in the agent environment, avoid pasting it into conversation text or shared files, and use a scoped key when possible. <br>


## Reference(s): <br>
- [Amap Open Platform](https://lbs.amap.com) <br>
- [Amap Web Service API Documentation](https://lbs.amap.com/api/webservice/summary) <br>
- [Amap REST API Endpoint](https://restapi.amap.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/770600682-cyber/amap-dinner-planner) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/770600682-cyber) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown-style planning response with ranked restaurant recommendations, commute comparisons, and a QR-code map reference.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AMAP_API_KEY environment variable and sends user-provided addresses, meeting areas, and restaurant preferences to Amap services for geocoding, search, routing, and map generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
