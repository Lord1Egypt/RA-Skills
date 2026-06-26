## Description: <br>
Plans customized walking routes from a user-provided location and desired distance, connects nearby parks, waterside paths, cafes, and other points of interest, then provides an Amap QR code for navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[770600682-cyber](https://clawhub.ai/user/770600682-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan walking, jogging, dog-walking, family stroll, and city-walk routes from natural-language location and distance requests. It returns a structured route card with points of interest, walking distances, estimated timing, weather context, and Amap navigation access. <br>

### Deployment Geography for Use: <br>
Global, where Amap Web Service APIs and map data are available. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Amap API key and sends user-provided route and location queries to Amap. <br>
Mitigation: Use an appropriately scoped API key, avoid sharing unnecessarily precise sensitive locations, and review Amap's service terms and privacy policy before use. <br>
Risk: Generated walking routes, POI details, weather context, and QR navigation links can be incomplete, stale, or unsuitable for current local conditions. <br>
Mitigation: Review the route in Amap before starting, verify safety and accessibility locally, and adjust the route when conditions or user constraints require it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/770600682-cyber/amap-walk-route) <br>
- [Amap Open Platform](https://lbs.amap.com) <br>
- [Amap Web Service API documentation](https://lbs.amap.com/api/webservice/summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Images, Guidance] <br>
**Output Format:** [Markdown route card with route details and an Amap QR code reference] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY and user-provided route/location details; sends route-related location queries to Amap.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
