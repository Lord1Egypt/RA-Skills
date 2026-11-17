## Description:

Fetch aviation weather data (METAR, TAF, PIREPs) from aviationweather.gov for flight planning, weather briefings, airport condition checks, and pilot-related weather queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimitryvin](https://clawhub.ai/user/dimitryvin)

### License/Terms of Use:


## Use Case:

External users, developers, and aviation operators can use this skill to retrieve current METAR observations, TAF forecasts, and nearby PIREPs for airport weather checks and flight-planning context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to aviationweather.gov using airport codes or latitude/longitude values supplied by the user.

Mitigation: Use the skill only when that network disclosure is acceptable, and provide only the location detail needed for the weather lookup.

Risk: The release evidence notes that a stricter manifest declaring the network scope would improve auditability.

Mitigation: Review the skill before deployment and consider adding explicit network-scope metadata for aviationweather.gov.

## Reference(s):

- [Aviation Weather API](https://aviationweather.gov/api/data)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands]

**Output Format:** [Markdown-style weather summaries or raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live aviationweather.gov responses for requested station IDs or latitude/longitude PIREP searches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
