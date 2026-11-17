## Description:

Daily weather forecast for any city or coordinates with a practical day plan (umbrella/sunscreen/layers tips and the best dry, comfortable outdoor window). Uses the free Open-Meteo API; no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwwdsb](https://clawhub.ai/user/lwwdsb)

### License/Terms of Use:

MIT

## Use Case:

People checking weather can use the skill to get a forecast for a chosen city or coordinates and practical advice about clothing, weather precautions, and a comfortable outdoor time window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete and flags that a stored home location may be sent to an external weather service without first asking; tool scope is undeclared.

Mitigation: Review the skill before installation, confirm that sending the selected location to Open-Meteo is expected, and avoid using a stored home location unless the user intends to share it.

## Reference(s):

- [A3 Weather Day Plan on ClawHub](https://clawhub.ai/lwwdsb/skills/a3-weather-lwwdsb)
- [Open-Meteo](https://open-meteo.com)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [Plain-text forecast summary or JSON forecast report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes current conditions, daily highs and lows, precipitation, wind, UV, practical tips, and an optional outdoor time window; forecast horizon is up to 7 days.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
