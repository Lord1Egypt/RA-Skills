## Description:

Comprehensive audit of all construction data sources and systems. Map data flows, identify silos, assess quality, and create integration roadmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction data, analytics, and operations teams use this skill to inventory project data sources, map integrations and data flows, identify silos, assess data quality, and plan an integration roadmap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle construction project metadata and local files provided by the user.

Mitigation: Confirm the intended input scope before use and provide explicit file paths instead of broad project-directory scans.

Risk: Spreadsheet exports can preserve untrusted survey values that begin with formula characters.

Mitigation: Sanitize or review values beginning with =, +, -, or @ before exporting Excel or CSV catalogs.

## Reference(s):

- [Data Driven Construction](https://datadrivenconstruction.io)
- [ClawHub skill listing](https://clawhub.ai/datadrivenconstruction/skills/data-source-audit)
- [ClawHub publisher profile](https://clawhub.ai/user/datadrivenconstruction)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with structured tables and optional CSV, Excel, or JSON export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include audit reports, data catalogs, integration matrices, quality scores, silo findings, and roadmap recommendations.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
