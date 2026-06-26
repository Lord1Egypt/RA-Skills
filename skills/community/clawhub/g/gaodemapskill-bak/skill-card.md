## Description: <br>
A skill to interact with Gaode Map (AMap) for location search and route planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Beelkic](https://clawhub.ai/user/Beelkic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search points of interest, geocode addresses, and plan driving, walking, bicycling, or transit routes through the Gaode Map API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location searches, addresses, coordinates, and route endpoints are sent to Gaode/AMap. <br>
Mitigation: Use the skill only when sharing those queries with Gaode/AMap is acceptable for the deployment. <br>
Risk: AMap API credentials could be exposed if passed directly on the command line. <br>
Mitigation: Use a dedicated restricted API key and provide it through the AMAP_API_KEY environment variable. <br>
Risk: The requests dependency is not pinned in requirements.txt. <br>
Mitigation: Pin or audit dependencies before repeatable or production installs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Beelkic/gaodemapskill-bak) <br>
- [AMap Console](https://console.amap.com/) <br>
- [AMap REST API endpoint](https://restapi.amap.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the tool.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, the requests package, and an AMAP_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
