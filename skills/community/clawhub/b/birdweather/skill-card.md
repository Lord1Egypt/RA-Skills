## Description: <br>
Query BirdWeather station data for species detections, trends, and comparisons from BirdNET-Pi and PUC bird song detection stations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxdraki](https://clawhub.ai/user/maxdraki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, birders, and wildlife-monitoring users can use this skill to query public BirdWeather station data, inspect recent detections, compare time periods, and summarize local bird activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BirdWeather API queries may reveal the station IDs, dates, periods, or species filters a user asks about. <br>
Mitigation: Use only station and query details that are acceptable to send to BirdWeather's public API. <br>
Risk: BirdNET AI classifications can misidentify species, and offline stations can produce empty or stale results. <br>
Mitigation: Treat unusual detections and empty result sets as signals to verify against station status, recent detections, or other observations before making decisions. <br>


## Reference(s): <br>
- [ClawHub BirdWeather Release](https://clawhub.ai/maxdraki/birdweather) <br>
- [BirdWeather Station App](https://app.birdweather.com/) <br>
- [BirdWeather API](https://app.birdweather.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output as plain text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key required; queries use public BirdWeather station data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
