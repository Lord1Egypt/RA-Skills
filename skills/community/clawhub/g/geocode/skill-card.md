## Description: <br>
Reverse geocode latitude/longitude to a human-readable region using geocode.com.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert latitude and longitude coordinates into concise human-readable locality and region output for low-frequency interactive lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coordinate lookups disclose each submitted latitude and longitude to geocode.com.cn or the configured GEOCODE_BASE_URL endpoint. <br>
Mitigation: Avoid sensitive exact locations unless disclosure is acceptable, or configure GEOCODE_BASE_URL to a trusted endpoint. <br>
Risk: Public endpoint use may be unsuitable for high-volume or automated batch geocoding. <br>
Mitigation: Use only low-frequency interactive lookups and avoid loops, bulk geocoding, or aggressive retries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jvy/geocode) <br>
- [Publisher profile](https://clawhub.ai/user/jvy) <br>
- [geocode.com.cn reverse geocoding endpoint](https://geocode.com.cn/) <br>
- [geocode.com.cn demo query](https://geocode.com.cn/?lat=39.9042&lon=116.4074) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON geocoding responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reverse geocoding only; responses may contain empty locality fields for remote or ambiguous coordinates.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
