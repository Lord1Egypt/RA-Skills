## Description:

Get current weather for a user-specified city and provide a short, practical weather briefing with the source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junjiehe-bot](https://clawhub.ai/user/junjiehe-bot)

### License/Terms of Use:

MIT-0

## Use Case:

People requesting a current weather briefing use this skill to get conditions and a practical recommendation for a specified city.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The user-specified city is sent to wttr.in to retrieve weather data.

Mitigation: Tell the user the city will be sent to wttr.in before fetching; avoid sending precise or sensitive location details.

## Reference(s):

- [wttr.in weather service](https://wttr.in/)
- [ClawHub release page](https://clawhub.ai/junjiehe-bot/skills/a3-weather-briefing)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Short Markdown weather briefing with current temperature, conditions, practical recommendation, and source attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current-condition data for one user-specified city.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
