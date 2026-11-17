## Description:

Find cheap flights, monitor prices, and alert on price drops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-focused agents use this skill to search Aerobase flight-deal data, compare fares by value and recovery impact, and create or review route watch alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight search and alert details are sent to Aerobase using AEROBASE_API_KEY.

Mitigation: Use the skill only when Aerobase API use is expected, keep the API key in the agent environment, and redact raw keys in outputs.

Risk: Quota and Pro feature claims may be promotional vendor messaging.

Mitigation: Present limits and pricing as vendor-provided information and direct users to Aerobase to confirm current terms.

Risk: Ongoing route-watch alert lifecycle details are unclear.

Mitigation: Confirm alert creation, listing, and management controls before relying on route watches.

## Reference(s):

- [Aerobase homepage](https://aerobase.app)
- [Aerobase OpenClaw travel agent](https://aerobase.app/openclaw-travel-agent)
- [ClawHub skill page](https://clawhub.ai/kurosh87/skills/aerobase-flight-deals)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown summaries with route, travel window, fare, airline, value score, recovery guidance, and follow-up actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Aerobase API responses and redacts raw API keys.]

## Skill Version(s):

3.2.1 (source: server release metadata; artifact frontmatter says 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
