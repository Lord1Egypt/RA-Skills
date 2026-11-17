## Description:

Daily Greeting Bot gets local weather and writes a humorous Chinese morning greeting or pickup line matched to the forecast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrencheski](https://clawhub.ai/user/wrencheski)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for a daily weather-aware morning greeting. The skill is intended for users who can provide a city and configure a weather API key for weather lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a weather API key and city name through curl, so users may disclose location context to their chosen weather API provider.

Mitigation: Use an approved weather API provider, keep WEATHER_API_KEY in the environment, and provide only location detail acceptable for the use case.

Risk: Weather lookup can fail because of network errors, invalid API credentials, or API availability.

Mitigation: Follow the artifact's fallback behavior by clearly explaining the lookup failure and returning a generic morning greeting.

Risk: The default output is a Chinese greeting, which may not match every user's language expectations.

Mitigation: Ask the agent to translate or adapt the greeting language when English or another language is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wrencheski/skills/daily-greeting-bot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style weather summary followed by a morning greeting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is normally in Chinese and depends on a user-provided city plus weather data from an API call.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
