## Description:

Search for local businesses worldwide via the discava API, returning structured business data with confidence scores and demand rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastian1747](https://clawhub.ai/user/sebastian1747)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find local businesses, service providers, restaurants, doctors, and tradespeople worldwide. It supports search, business details, rankings, autocomplete suggestions, and data-quality feedback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interactive HTML cards may include third-party click tracking.

Mitigation: Prefer JSON responses and local rendering unless the user specifically needs HTML cards and understands the tracking behavior.

Risk: Precise latitude and longitude can expose sensitive location context.

Mitigation: Use city or country filters by default and send coordinates only when they are necessary for distance-based results.

Risk: Feedback comments are stored free text and may accidentally include sensitive personal details.

Mitigation: Keep feedback factual and minimal, and omit personal, confidential, or unnecessary identifying information.

## Reference(s):

- [discava Skill on ClawHub](https://clawhub.ai/sebastian1747/skills/discava)
- [discava API](https://discava.ai/api/v1)
- [OpenStreetMap](https://www.openstreetmap.org)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses may include business contact details, location data, rankings, suggestions, and optional HTML cards; service use is rate limited to 500 requests per hour per IP.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
