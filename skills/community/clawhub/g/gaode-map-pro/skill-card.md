## Description: <br>
Provides zero-configuration Gaode/Amap map capabilities for geocoding, POI search, routing, weather, IP location, distance, static maps, coordinate conversion, and app-deep-link actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent answer map, location, route-planning, weather, nearby-place, and Amap app-link requests through a Gaode/Amap proxy workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map queries can include addresses, coordinates, route endpoints, search terms, and IP lookup data that pass through the skill publisher's cloud proxy. <br>
Mitigation: Avoid highly sensitive locations unless the user trusts the proxy and its stated no-storage behavior. <br>
Risk: Generated navigation or taxi app links may not complete an action in a pure chat environment or on devices without the Gaode/Amap app installed. <br>
Mitigation: Treat app-link outputs as handoff links and confirm them on a compatible user device before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/gaode-map-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/travel-skills) <br>
- [Gaode proxy endpoint](https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Guidance] <br>
**Output Format:** [JSON responses and text guidance from map lookup, routing, search, weather, and app-link tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls accept JSON parameters and may return route details, POI data, weather data, coordinates, distances, static map URLs, or Amap app URI links.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and artifact/version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
