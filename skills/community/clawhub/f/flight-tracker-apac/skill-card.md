## Description:

Check flight schedules between supported airports, show timings, terminals, gates, delays, aircraft details, and optional departure countdowns using a local Python script backed by the Aviationstack API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caddytan](https://clawhub.ai/user/caddytan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to check flight schedules between supported IATA airports, especially APAC routes and selected long-haul routes. It helps summarize operating flights, timing, terminals, gates, status, delays, aircraft details, and optional departure countdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends route lookup parameters and the Aviationstack API key to Aviationstack over HTTPS.

Mitigation: Install only if that data sharing is acceptable, keep ~/.openclaw/.env private, and do not commit the API key to source control.

Risk: When no API key is configured, fallback links include route codes for Google Flights and FlightRadar24.

Mitigation: Use the fallback links only for routes that are acceptable to share with those external services.

Risk: The skill is limited to the airport codes built into the script and does not perform booking or fare comparison.

Mitigation: Use it for schedule lookup only, and verify unsupported routes or booking decisions with a dedicated travel service.

## Reference(s):

- [Flight Tracker for Airports in Asia Pacific on ClawHub](https://clawhub.ai/caddytan/skills/flight-tracker-apac)
- [caddytan ClawHub profile](https://clawhub.ai/user/caddytan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown summary with inline shell commands and plain-text flight details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include manual HTTPS lookup links when AVIATIONSTACK_API_KEY is not configured.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
