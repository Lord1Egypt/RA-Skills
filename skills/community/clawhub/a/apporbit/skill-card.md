## Description:

Analyze AppOrbit's published App Store and Google Play chart observations and app metadata for historical rankings, rank movement, app lookup, and market coverage; observations are not live ranks or download estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivershuo](https://clawhub.ai/user/ivershuo)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to examine published historical app-store rankings, compare rank movements, look up apps, and assess chart coverage with source citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads public data over the network, or from an optional user-specified source; untrusted source settings may lead to untrustworthy analysis.

Mitigation: Use the disclosed default sources or a trusted local dataset; do not set APPORBIT_SOURCE or APPORBIT_SITE_DIR to untrusted locations.

Risk: Historical observations or delayed website metadata may be mistaken for current store rankings.

Mitigation: Report snapshot capture time, coverage, and data status; cite the immutable snapshot for ranking claims and do not describe observations as live.

## Reference(s):

- [AppOrbit data format v1](references/data-format.md)
- [AppOrbit published data](https://raw.githubusercontent.com/ivershuo/apporbit/data/v1/)
- [AppOrbit current data format](https://raw.githubusercontent.com/ivershuo/apporbit/main/docs/data-format.md)
- [Snapshot schema](https://raw.githubusercontent.com/ivershuo/apporbit/data/v1/schemas/snapshot-v1.schema.json)
- [Run schema](https://raw.githubusercontent.com/ivershuo/apporbit/data/v1/schemas/run-v1.schema.json)
- [AppOrbit website](https://apporbit.ooxxz.com/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Markdown analysis with source links; JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical observations include capture dates and chart coverage; results are not live rankings or download estimates.]

## Skill Version(s):

1.0.0 (source: ClawHub release; bundled metadata says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
