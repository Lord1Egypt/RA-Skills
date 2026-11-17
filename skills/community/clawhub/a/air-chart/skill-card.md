## Description:

Query global air-quality measurements from OpenAQ and render trend and comparison charts with x-cmd Draw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiakai](https://clawhub.ai/user/qiakai)

### License/Terms of Use:

MIT

## Use Case:

People analyzing local or global air quality use the skill to compare pollutant measurements across cities, stations, or time periods and share a chart with its measurement summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is incomplete and rates the release suspicious with medium confidence; its guidance also flags an unpinned installation instruction and the possibility of misleading chart comparisons.

Mitigation: Review the source before installing, pin the installation reference, and check station selection, units, timestamps, and guideline context before relying on comparisons.

## Reference(s):

- [OpenAQ API v3](https://api.openaq.org/v3)
- [x-cmd Draw](https://x-cmd.com/draw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown with a shareable chart URL and measurement summary; optional SVG or PNG chart file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries include pollutant units and station context; charts show WHO guideline references when units permit.]

## Skill Version(s):

1.6.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
