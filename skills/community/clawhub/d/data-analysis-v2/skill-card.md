## Description:

Data analysis and visualization. Query databases, generate reports, automate spreadsheets, and turn raw data into clear, actionable insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janeaaaa](https://clawhub.ai/user/janeaaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business teams use this skill to plan and explain data analysis from SQL, spreadsheets, notebooks, dashboards, exports, or ad hoc tables. It supports KPI debugging, experiment readouts, funnel and cohort analysis, anomaly reviews, executive reporting, metric quality checks, chart selection, and decision briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The active agent may receive sensitive datasets, credentials, or business data while performing analysis.

Mitigation: Use the skill only in an agent environment appropriate for the data, and avoid pasting sensitive datasets or credentials unless that environment is approved for them.

Risk: Analysis outputs can become misleading when metric definitions, sample sizes, comparison groups, or confounders are weak.

Mitigation: Require metric contracts, uncertainty, baseline checks, caveats, and escalation when the data cannot support the requested claim.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/janeaaaa/skills/data-analysis-v2)
- [Skill homepage](https://clawic.com/skills/data-analysis)
- [Metric Contracts](artifact/metric-contracts.md)
- [Chart Selection](artifact/chart-selection.md)
- [Decision Briefs](artifact/decision-briefs.md)
- [Analytical Pitfalls](artifact/pitfalls.md)
- [Analysis Techniques](artifact/techniques.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, query, shell command, configuration, table, and decision-brief snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no external network requests, hidden persistence, background jobs, or required local setup are declared.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
