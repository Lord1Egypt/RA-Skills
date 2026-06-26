## Description: <br>
Access BirdWeather PUC station data for species detections, sensor readings, historical trends, and new-species alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent query a BirdWeather PUC station for recent detections, species summaries, environmental sensor readings, new-species alerts, and optional local trend logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad bird-related prompts may activate the skill when the user did not intend to query BirdWeather station data. <br>
Mitigation: Prefer explicit prompts that mention BirdWeather, the station token, or the specific station action. <br>
Risk: Station tokens are public read-only identifiers but can still expose station observations if shared unintentionally. <br>
Mitigation: Pass tokens per invocation or through the environment and avoid including them in shared summaries or logs. <br>
Risk: Optional trend logging writes BirdWeather sensor and species records to a local SQLite database path. <br>
Mitigation: Use an intended local database path and review stored records before sharing the database. <br>


## Reference(s): <br>
- [BirdWeather API Reference](references/api.md) <br>
- [BirdWeather station API](https://app.birdweather.com/api/v1/stations/{token}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make read-only BirdWeather API calls and optionally write SQLite history to a user-specified database path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
