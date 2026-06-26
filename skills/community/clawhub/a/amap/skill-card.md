## Description: <br>
Provides agent guidance for using the Gaode (Amap) Web Service API for location search, weather queries, route planning, geocoding, reverse geocoding, and administrative code lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dboy233](https://clawhub.ai/user/Dboy233) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to prepare Amap Web Service API calls for user-requested map, weather, address, coordinate, and driving-route tasks. It requires a user-provided Amap API key in AMAP_KEY and curl for command execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends relevant locations, addresses, coordinates, route endpoints, and search keywords to Amap. <br>
Mitigation: Avoid querying highly sensitive locations unless necessary, and inform users when their requested data will be sent to Amap. <br>
Risk: The skill depends on an Amap API key exposed through the AMAP_KEY environment variable. <br>
Mitigation: Use a dedicated Amap API key where possible, and keep AMAP_KEY out of shared logs, shell history, and public artifacts. <br>


## Reference(s): <br>
- [Amap Open Platform](https://lbs.amap.com/) <br>
- [ClawHub amap release](https://clawhub.ai/Dboy233/amap) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_KEY and sends user-requested location, address, coordinate, weather, routing, and search data to Amap.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
