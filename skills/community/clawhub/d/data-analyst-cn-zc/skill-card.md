## Description:

Chinese-language data analysis assistant for data cleaning, statistical analysis, visualization guidance, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Data analysts, product managers, and operations teams use this skill to structure common data cleaning, statistical analysis, visualization, and reporting workflows in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples may read local files, databases, or external APIs.

Mitigation: Review and adapt code before execution, use approved data sources, and avoid sending confidential data to third-party services without permission.

Risk: Analysis, statistics, and visualizations may be incomplete or misleading without business validation.

Mitigation: Validate results against the source data, domain expectations, and the business question before acting on recommendations.

Risk: Large data sets may cause memory pressure when using the provided pandas-style examples.

Mitigation: Use sampling, chunked processing, or more scalable tooling for large files, and keep backups before cleaning or transforming data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/data-analyst-cn-zc)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Python code blocks and analysis-report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are prompt guidance and example Python snippets for pandas, matplotlib, seaborn, sqlite3, requests, and statsmodels workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
