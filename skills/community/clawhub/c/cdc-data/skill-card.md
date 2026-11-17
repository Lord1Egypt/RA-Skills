## Description:

Locates, verifies, optionally downloads, and extracts official China CDC influenza, respiratory, COVID-19, and infectious-disease risk reports for requested periods or latest releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaoshou.dev](https://clawhub.ai/user/miaoshou.dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to find, verify, download, and extract official China CDC health reports by report type, week, month, issue, publication date, reference date, or latest release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF extraction installs and uses an unpinned pdfplumber dependency range.

Mitigation: Use an isolated environment and pin or hash-verify pdfplumber before installing requirements.txt.

Risk: The skill accesses official China CDC pages and can write report artifacts locally.

Mitigation: Run it only when official China CDC access and local artifact writes are acceptable, and review saved artifact paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miaoshou.dev/skills/cdc-data)
- [China CDC official site](https://www.chinacdc.cn/)
- [Source registry](references/source-registry.md)
- [Workflow](references/workflow.md)
- [Output protocol](references/output-schema.md)
- [Artifact storage](references/artifact-schema.md)
- [Matching and time rules](references/matching-rules.md)
- [PDF extraction rules](references/pdf-extraction-rules.md)
- [Metric schema](references/metric-schema.md)
- [Source schema](references/source-schema.md)
- [China influenza weekly adapter](references/adapters/influenza-weekly.md)
- [Respiratory weekly adapter](references/adapters/respiratory-weekly.md)
- [COVID-19 monthly adapter](references/adapters/covid-monthly.md)
- [Global infectious risk monthly adapter](references/adapters/global-infectious-risk-monthly.md)
- [China public health risk monthly adapter](references/adapters/china-public-health-risk-monthly.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Concise text responses with optional JSON extraction artifacts and saved PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses explicit status values, verified report URLs, warnings, saved paths, and permitted next actions.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
