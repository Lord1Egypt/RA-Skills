## Description:

Provides structured weather information for specified cities and dates, including temperature, humidity, wind, precipitation, perceived temperature, and practical advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shilingong](https://clawhub.ai/user/shilingong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to parse weather requests by city and date, call or simulate a weather lookup, and return structured weather data with clothing or travel advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups may send city and date requests to a configured weather provider.

Mitigation: Confirm the selected provider and data-sharing expectations before installation or use.

Risk: API keys could be exposed if placed directly in prompts or examples.

Mitigation: Configure weather provider credentials through the host platform or another secret-management mechanism.

Risk: Simulated weather data may be used when no real API is available.

Mitigation: Use a real weather provider for decisions that require current or accurate weather conditions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shilingong/skills/city-weathers)
- [API integration notes](artifact/api.md)
- [Tool schema](artifact/tool.json)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Guidance]

**Output Format:** [Structured JSON with weather fields and short human-facing advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [City is required; date defaults to today and supports today, tomorrow, after_tomorrow, or 7d.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
