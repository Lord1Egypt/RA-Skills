## Description: <br>
Get Croatian weather data, forecasts, and alerts from DHMZ (meteo.hr) - no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[faleksic](https://clawhub.ai/user/faleksic) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Claude Code users use this skill to fetch and summarize Croatian weather observations, forecasts, alerts, and related public DHMZ data without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live requests to Croatian public weather sites. <br>
Mitigation: Install only if live public-network requests are acceptable in the target environment. <br>
Risk: If no city is supplied, the skill may infer a city from conversation context or default to Zagreb. <br>
Mitigation: Provide the desired city explicitly when location inference is not wanted. <br>


## Reference(s): <br>
- [DHMZ XML Data for Users](https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici) <br>
- [DHMZ](https://meteo.hr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries with curl commands and XML weather data references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and fetches public Croatian weather XML; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
