## Description:

Assess construction data quality using completeness, accuracy, consistency, timeliness, and validity metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, data teams, and construction project analysts use this skill to evaluate user-provided construction datasets, summarize quality issues, and prepare validation reports or export guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project files supplied by the user and may process sensitive construction data.

Mitigation: Install only when filesystem access to the referenced project data is acceptable, and limit inputs to files intended for analysis.

Risk: Generated quality reports can contain sensitive construction data.

Mitigation: Treat exported reports as local sensitive files and review them before sharing.

Risk: Sample validation logic may be insufficient for financial, compliance, or safety decisions.

Mitigation: Review and adapt thresholds, regex patterns, and rules before relying on outputs for high-impact decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/skills/data-quality-check)
- [DataDrivenConstruction Homepage](https://datadrivenconstruction.io)
- [Great Expectations](https://greatexpectations.io)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, configuration, files]

**Output Format:** [Markdown with structured tables, Python examples, and optional report/export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local CSV, Excel, or JSON report guidance when requested by the user.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
