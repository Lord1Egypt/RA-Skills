## Description:

Structures cohort analyses for retention, LTV, behavioral segmentation, churn indicators, and prioritized interventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, growth teams, and data analysts use this skill to structure retention, LTV, churn, or behavioral cohort analyses from supplied product data or schemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing or incomplete product data can make cohort outputs framework-only rather than decision-ready.

Mitigation: Ask for the analysis goal, cohort definition, observation window, key metric, available data, and baseline before producing results; clearly mark placeholders and data gaps.

Risk: Unadapted SQL placeholders or an unconfirmed SQL dialect can produce unusable queries.

Mitigation: Adapt table names, column names, key events, dates, and dialect-specific date functions to the user's supplied schema before use.

Risk: One trigger phrase is truncated, which may make activation slightly less polished.

Mitigation: Users can invoke the skill with explicit requests such as running cohort analysis, analyzing retention by acquisition month, or calculating LTV by acquisition period.

## Reference(s):

- [Cohort Analysis ClawHub page](https://clawhub.ai/mohitagw15856/skills/cohort-analysis)
- [Cohort Analysis homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/cohort-analysis.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with tables, chart JSON blocks, and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses clearly marked placeholders when source data or schemas are missing; does not fabricate metrics, benchmarks, or lift estimates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
