## Description:

Build comprehensive GEO performance reports with executive summaries, platform breakdowns, competitive analysis, and strategic action plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn GEO metrics into structured performance reports covering executive summaries, platform breakdowns, competitive position, insights, and action plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command example and bundled Python script do not fully match, which may confuse users expecting brand, period, or output-file arguments.

Mitigation: Check the script interface before running it and pass only the supported metrics JSON input unless the script is updated.

Risk: Generated GEO recommendations can be misleading when the provided metrics are incomplete or not intended for the report.

Mitigation: Provide only intended metrics files and review the generated report before using it for business decisions.

## Reference(s):

- [Report Structure Guide](references/structure-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/geoly-geo/skills/geo-report-builder)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown reports with tables, summaries, and action-plan sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reads a local JSON metrics file and prints the generated report to standard output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
