## Description:

Connects to Garmin Connect to summarize personal health and activity trends, view calendar events, manage Jet Lag Adviser trips, and generate interactive charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bolinches](https://clawhub.ai/user/bolinches)

### License/Terms of Use:

MIT-0

## Use Case:

Garmin Connect users and their assistants use this skill to explore sleep, HRV, recovery, and workouts, review trips and events, and create optional health dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Garmin account credentials and locally stored session tokens could expose personal health data.

Mitigation: Use OpenClaw-managed environment credentials rather than a plaintext config file, and protect local session tokens.

Risk: Adding, replacing, or deleting a trip changes the Garmin account; replacement may remove omitted flights.

Mitigation: Review trip details and preview output, then explicitly approve any trip creation, replacement, or deletion before execution.

Risk: Wearable health readings may be incomplete or inaccurate and should not be treated as a diagnosis.

Mitigation: Present trends as informational and direct health concerns to a qualified clinician.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bolinches/skills/garmin-health-analysis-2)
- [Garmin Connect API reference](artifact/references/api.md)
- [Health analysis guide](artifact/references/health_analysis.md)
- [Extended capabilities](artifact/references/extended_capabilities.md)
- [python-garminconnect library](https://github.com/cyberjunky/python-garminconnect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown responses, JSON data, and optional HTML dashboards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trip replacements and deletions require a preview and explicit confirmation.]

## Skill Version(s):

1.6.1 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
