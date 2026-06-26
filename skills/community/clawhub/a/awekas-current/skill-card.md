## Description: <br>
Fetches and normalizes current weather data from the AWEKAS API with caching, retries, timeouts, and structured error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michik1712](https://clawhub.ai/user/michik1712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and weather automation users can call this skill from an OpenClaw agent to retrieve current AWEKAS station weather and receive a normalized JSON response for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AWEKAS API key, and mishandled credentials could expose access to the weather service account. <br>
Mitigation: Use a dedicated or easily revocable API key, pass it through an environment variable when possible, and avoid sharing logs or error traces that may include request details. <br>


## Reference(s): <br>
- [AWEKAS Wetter API on ClawHub](https://clawhub.ai/michik1712/awekas-current) <br>
- [AWEKAS current weather API endpoint](https://api.awekas.at/current.php) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [JSON object with normalized weather fields and structured error objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AWEKAS API key through the key argument or AWEKAS_KEY environment variable; accepts an optional station argument; caches responses for 60 seconds and uses request retries with an 8-second timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
