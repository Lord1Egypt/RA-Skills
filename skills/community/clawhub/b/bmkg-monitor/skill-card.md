## Description:

Monitoring earthquake, weather, and tsunami data in Indonesia using BMKG official data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluemeda](https://clawhub.ai/user/bluemeda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve and summarize BMKG earthquake, tsunami-potential, weather forecast, and active warning data for Indonesia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public BMKG data services when earthquake, weather, tsunami, or warning data is requested.

Mitigation: Use in environments where these outbound BMKG endpoints are allowed, or add explicit endpoint allowlist controls before deployment.

Risk: BMKG data is live public hazard information and may change as official reports are updated.

Mitigation: Treat returned earthquake, tsunami, weather, and warning data as time-sensitive and verify critical safety decisions against official BMKG channels.

## Reference(s):

- [BMKG Monitor on ClawHub](https://clawhub.ai/bluemeda/skills/bmkg-monitor)
- [bluemeda publisher profile](https://clawhub.ai/user/bluemeda)
- [Seismology Reference](references/seismology.md)
- [BMKG earthquake data](https://data.bmkg.go.id/DataMKG/TEWS/)
- [BMKG weather forecast API](https://api.bmkg.go.id/publik/prakiraan-cuaca)
- [BMKG weather warnings](https://www.bmkg.go.id/alerts/nowcast/id)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public BMKG data on request; no credentials were detected in server security evidence.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
