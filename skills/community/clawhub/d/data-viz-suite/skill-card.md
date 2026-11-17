## Description:

Data Viz Suite helps agents generate static charts, interactive dashboards, and business reports using Plotly, Matplotlib, and Seaborn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to create charts, dashboards, and exportable reports from tabular business data. It is suited for agent workflows that need Python visualization code, report-generation guidance, or generated BI artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated dashboards and reports may run unsafe injected content when untrusted titles, table cells, KPI labels, or report text are rendered as HTML.

Mitigation: Use only trusted data or escape and sanitize user-controlled text before generating or opening HTML outputs.

Risk: Generated dashboards may contact a mutable third-party Plotly CDN when opened.

Mitigation: Use a pinned, trusted Plotly asset or vendor the JavaScript dependency for environments that require reproducible or offline review.

Risk: Dependency versions are specified as ranges rather than a reproducible lockfile.

Mitigation: Install from a reviewed lockfile or pinned dependency set before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/data-viz-suite)
- [Project homepage from ClawHub metadata](https://github.com/openclaw/skills/tree/main/data-viz-suite)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of HTML dashboards, chart image exports, PDF reports, and Excel reports.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
