## Description: <br>
高德打车 provides Gaode map taxi launch, route planning, nearby search, POI lookup, geocoding, weather, IP-location, distance, static map, coordinate conversion, and navigation-link tools for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent to search Gaode locations, plan travel routes, estimate taxi options, and generate Gaode app taxi or navigation links. Developers can use the skill to expose map and mobility lookups through agent tool calls without manual proxy setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches, addresses, coordinates, IP-location queries, and taxi route details are sent to the skill publisher's cloud proxy for Gaode lookups. <br>
Mitigation: Use the skill only when users accept that location and route details will be sent to that proxy, and avoid sensitive home, workplace, or private itinerary details unless the proxy operator is trusted. <br>
Risk: Taxi prices and route information can be estimates or depend on Gaode app availability on the user's device. <br>
Mitigation: Treat taxi costs and route details as planning guidance, and confirm final fare and ride execution in the Gaode app. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/gaode-taxi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Guidance] <br>
**Output Format:** [JSON tool responses with concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Gaode app taxi or navigation URIs, route details, estimated taxi costs, POI results, weather data, coordinates, and static map URLs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence release.version and artifact/version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
