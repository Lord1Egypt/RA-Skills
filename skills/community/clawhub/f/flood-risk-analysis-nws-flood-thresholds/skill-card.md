## Description:

Download flood stage thresholds from NWS (National Weather Service). Use when determining flood levels for USGS stations, accessing action/minor/moderate/major flood stages, or matching stations to their flood thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to obtain NWS flood stage thresholds, match them to USGS station IDs, and prepare threshold data for flood-risk analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flood threshold data may be stale or unavailable for some stations.

Mitigation: Review output data freshness and handle missing NWS thresholds before using results in flood-risk decisions.

Risk: NWS data may contain sentinel values such as -9999 or rows with unexpected column counts.

Mitigation: Filter sentinel values, coerce threshold columns to numeric values, and truncate CSV rows to the documented header count before analysis.

## Reference(s):

- [NWS/NWPS All Gauges CSV](https://water.noaa.gov/resources/downloads/reports/nwps_all_gauges_report.csv)
- [NWS/NWPS Gauge Page Example](https://water.noaa.gov/gauges/04118105)
- [ClawHub Skill Page](https://clawhub.ai/wu-uk/skills/flood-riREDACTED-SECRET)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to fetch public NWS data, parse CSV rows, filter sentinel values, and match thresholds by USGS station ID.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
