## Description: <br>
Provides AMap-based geocoding, reverse geocoding, POI search, route planning, and distance measurement for location-related agent requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronjager92](https://clawhub.ai/user/aaronjager92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer map and location questions by calling AMap services for addresses, coordinates, nearby places, routes, and distances. It is intended for workflows where sending the requested location data to AMap is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches, addresses, and coordinates may be sent to AMap when the skill is used. <br>
Mitigation: Avoid sending home, workplace, or other sensitive precise locations unless needed, and invoke the skill only for explicit map or location requests. <br>
Risk: The skill depends on user-provided AMap credentials. <br>
Mitigation: Store the API key and optional secret key in environment variables or a local configuration file that is not published with the skill. <br>


## Reference(s): <br>
- [AMap developer key console](https://console.amap.com/dev/key/app) <br>
- [Artifact reference README](artifact/references/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/aaronjager92/amap-geoservice) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AMap API key; some route and distance operations may also require a configured AMap secret key for request signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
