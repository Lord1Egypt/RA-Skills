## Description: <br>
Provides AMap-based real-time traffic lookup and driving route planning using AMap traffic, geocoding, and driving direction APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robin797860](https://clawhub.ai/user/Robin797860) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check traffic conditions, geocode trip endpoints, and compare driving routes with estimated time, distance, cost, and congestion details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends addresses, coordinates, and route endpoints to AMap when resolving locations and planning routes. <br>
Mitigation: Avoid submitting sensitive home, work, or private locations unless sharing them with AMap is acceptable. <br>
Risk: The skill requires an AMap API key that may be read from OpenClaw configuration or the AMAP_KEY environment variable. <br>
Mitigation: Use a dedicated restricted API key where possible and keep the OpenClaw configuration file private. <br>


## Reference(s): <br>
- [Amap Traffic Skill Page](https://clawhub.ai/Robin797860/amap-traffic) <br>
- [Amap Open Platform Console](https://console.amap.com/) <br>
- [AMap Geocoding API Endpoint](https://restapi.amap.com/v3/geocode/geo) <br>
- [AMap Driving Direction API Endpoint](https://restapi.amap.com/v3/direction/driving) <br>
- [AMap Traffic Status API Endpoint](https://restapi.amap.com/v3/traffic/status/road) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text route and traffic summaries, with setup guidance and command examples in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AMap API key and user-provided origin, destination, and optional city values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
