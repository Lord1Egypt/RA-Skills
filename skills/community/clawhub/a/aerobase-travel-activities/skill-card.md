## Description:

Discover near-airport and destination activities with ratings, reviews, and booking context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:

MIT

## Use Case:

External travel agents and assistants use this skill to find destination attractions, tours, and restorative layover activities that fit a traveler’s budget, time, and recovery needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on Aerobase as the activity recommendation source.

Mitigation: Use it when Aerobase is an acceptable source for the travel context, and review recommendations for traveler fit before presenting them as final advice.

Risk: The skill requires an Aerobase API key and may surface signup or paid-plan information on authentication or quota errors.

Mitigation: Store the API key in the AEROBASE_API_KEY environment variable, redact keys in outputs, and disclose quota or plan guidance plainly when it affects the response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kurosh87/skills/aerobase-travel-activities)
- [Aerobase homepage](https://aerobase.app)
- [Aerobase OpenClaw travel agent](https://aerobase.app/openclaw-travel-agent)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked activity options, timing and travel-friction notes, follow-up actions, and authentication or quota guidance.]

## Skill Version(s):

3.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
