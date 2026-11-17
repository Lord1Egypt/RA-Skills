## Description:

Profile construction data to understand characteristics, distributions, quality metrics, and patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction data teams, developers, and analysts use this skill to profile CSV, Excel, JSON, or directly provided construction data before ETL, quality monitoring, schema validation, and anomaly review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated profiles may expose sensitive project metadata, column names, top values, and summary statistics from source data.

Mitigation: Review profile outputs before sharing or exporting them, and handle them under the same data controls as the source dataset.

Risk: Python dependency differences can change profiling behavior or reproducibility.

Mitigation: Run the skill in an isolated Python environment and pin pandas and numpy versions when repeatable results matter.

## Reference(s):

- [Data Profiler on ClawHub](https://clawhub.ai/datadrivenconstruction/skills/data-profiler)
- [datadrivenconstruction Publisher Profile](https://clawhub.ai/user/datadrivenconstruction)
- [Data Driven Construction](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured tables, JSON-ready profile dictionaries, and Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated profiles can include column names, top values, null rates, quality issues, summary statistics, recommendations, and comparison results.]

## Skill Version(s):

2.1.0 (source: server release evidence; artifact/claw.json reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
