## Description: <br>
Provides Singapore bus arrival guidance from a source location to a destination using public transit and geocoding APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhayjb](https://clawhub.ai/user/abhayjb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents can use this skill to interpret natural-language Singapore bus trip requests, identify suitable nearby stops and routes, and return live arrival details with seating and vehicle information. <br>

### Deployment Geography for Use: <br>
Singapore <br>

## Known Risks and Mitigations: <br>
Risk: Origin and destination text may be sent to third-party Singapore transit and geocoding APIs. <br>
Mitigation: Avoid entering sensitive exact home or work locations unless that sharing is acceptable. <br>
Risk: The bundled shell script depends on local command-line tools to fetch and parse live arrival data. <br>
Mitigation: Ensure curl and jq are installed before running the script directly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abhayjb/buslah) <br>
- [OneMap geocoding API](https://www.onemap.gov.sg/api/common/elastic/search) <br>
- [BusRouter bus stops data](https://busrouter.sg/data/2/bus-stops.json) <br>
- [BusRouter routes data](https://busrouter.sg/data/2/routes.json) <br>
- [ArriveLah live arrivals API](https://arrivelah2.busrouter.sg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with bus service, arrival time, load, vehicle type, and stop details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use configured default stop, service, destination, and API URL when running the bundled shell script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
