## Description:

Austrian public transport (VOR AnachB) skill for querying real-time departures, searching stations and stops, planning routes, and checking service disruptions across Austria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manmal](https://clawhub.ai/user/manmal)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer Austrian public transport questions, including finding stops, checking real-time departures, planning routes between stations, and reviewing service disruptions.

### Deployment Geography for Use:

Austria

## Known Risks and Mitigations:

Risk: Untrusted web or chat input could be passed into shell scripts without robust validation.

Mitigation: Prefer normal station IDs and small numeric counts; add input validation, JSON-safe request construction, request timeouts, and result limits before exposing the scripts to untrusted inputs.

Risk: Live transit lookups depend on an external HAFAS endpoint and time-sensitive real-time data.

Mitigation: Treat results as current lookup guidance and verify critical journeys against an official transit source before travel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manmal/skills/a-nach-b)
- [VOR AnachB HAFAS API endpoint](https://vao.demo.hafas.de/gate)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [JSON responses from bash scripts, with concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live public-transport results depend on upstream HAFAS availability and real-time data quality.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
