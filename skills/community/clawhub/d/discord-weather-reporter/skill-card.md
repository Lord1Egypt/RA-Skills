## Description:

Fetch weather forecasts and current conditions, formatted for Discord display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for current weather conditions, multi-day forecasts, precipitation checks, snow checks, and weather alerts formatted for Discord display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled locations may be placed into curl commands without validation or URL encoding.

Mitigation: Validate or URL-encode location values and invoke HTTP requests without shell interpolation.

Risk: Weather requests may disclose sensitive or precise private locations to wttr.in.

Mitigation: Avoid sending sensitive or precise private locations unless the user is comfortable sharing them with wttr.in.

## Reference(s):

- [Discord Weather Reporter on ClawHub](https://clawhub.ai/fuzzyb33s/skills/discord-weather-reporter)
- [fuzzyb33s ClawHub profile](https://clawhub.ai/user/fuzzyb33s)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and Discord-ready weather text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses wttr.in and requires no API key; location input should be validated or URL-encoded before use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
