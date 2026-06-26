## Description: <br>
Amap Map lets agents call Amap/Gaode Maps Web Services for POI search, nearby search, POI details, walking, bicycling, driving routes, geocoding, and reverse geocoding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klscool](https://clawhub.ai/user/klscool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search places, inspect POI details, plan walking, bicycling, or driving routes, and convert between addresses and coordinates through Amap/Gaode Maps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches, addresses, coordinates, and route endpoints are sent to Amap. <br>
Mitigation: Avoid submitting sensitive home, workplace, or real-time travel details unless sharing them with Amap is acceptable. <br>
Risk: The skill uses an Amap Web Services API key and tracks local usage against a daily quota. <br>
Mitigation: Use a dedicated API key, keep it out of prompts and logs, and monitor quota usage in the Amap console. <br>


## Reference(s): <br>
- [Amap Open Platform](https://lbs.amap.com/) <br>
- [Amap Web Services API](https://restapi.amap.com/v3) <br>
- [Amap Developer Console](https://console.amap.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON API responses and markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Amap Web Services API key; local usage statistics are recorded by the script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
