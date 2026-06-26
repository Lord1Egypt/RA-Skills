## Description: <br>
Amap Travel Planner helps agents create travel itineraries using AMap route planning, place search, budget estimates, checklist guidance, and map QR-code generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[770600682-cyber](https://clawhub.ai/user/770600682-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning assistants use this skill to turn natural-language trip goals into route-aware itineraries, budget summaries, transportation comparisons, and AMap map links. It is most relevant for trips where AMap coverage and Web Service API data are appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AMap API key and may consume quota or expose key misuse if credentials are broadly scoped. <br>
Mitigation: Use a scoped or quota-limited AMap API key, store it only in the expected AMAP_API_KEY environment variable, and monitor API usage. <br>
Risk: Trip planning sends addresses and locations to AMap for geocoding, routing, and map generation. <br>
Mitigation: Avoid entering sensitive private addresses unless the user is comfortable sharing them with AMap for those services. <br>


## Reference(s): <br>
- [Amap Travel Planner on ClawHub](https://clawhub.ai/770600682-cyber/amap-travel-planner) <br>
- [Publisher profile](https://clawhub.ai/user/770600682-cyber) <br>
- [AMap Open Platform](https://lbs.amap.com) <br>
- [AMap Web Service API documentation](https://lbs.amap.com/api/webservice/summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown itinerary, budget, checklist, route comparison, and map-link guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AMap route data, distances, durations, estimated costs, and QR-code or schema links when the configured AMap API key permits them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
