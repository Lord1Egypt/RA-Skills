## Description:

Access BirdWeather PUC station data for species detections, sensor readings, and historical trends using a BirdWeather station token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve BirdWeather station detections, summarize recent backyard bird activity, inspect PUC environmental sensor readings, and maintain optional local trend history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A BirdWeather station token identifies a public read-only station and allows station detections and sensor readings to be queried.

Mitigation: Use only the intended station token, avoid sharing command transcripts that include the token, and rotate or replace the station token if it is exposed beyond the intended audience.

Risk: Optional SQLite logging can retain local sensor and species history over time.

Mitigation: Write the database only to a user-chosen path, enable recurring logging only when local history retention is desired, and delete or protect the database according to local retention needs.

## Reference(s):

- [BirdWeather API Reference](references/api.md)
- [BirdWeather station API](https://app.birdweather.com/api/v1/stations/{token})
- [ClawHub release page](https://clawhub.ai/pfrederiksen/skills/birdweather-puc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided BirdWeather station token and can optionally write local SQLite history to a user-specified database path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
