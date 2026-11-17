## Description:

Generates Chinese-language data analysis reports from common tabular data formats with statistics, charts, key insights, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiyongwang](https://clawhub.ai/user/ruiyongwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users use this skill to inspect CSV, Excel, JSON, TSV, or DataFrame data and produce concise Chinese-language reports with quality checks, statistical summaries, visualizations, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes user-provided datasets and may generate misleading conclusions if the input data is incomplete, biased, malformed, or misunderstood.

Mitigation: Review generated statistics, charts, and recommendations against the source data before using them for decisions.

Risk: The skill depends on local Python data-analysis libraries that may vary by environment.

Mitigation: Use a virtual environment and review or pin dependencies before installation or repeated production use.

Risk: Sensitive datasets may be exposed if users point the skill at files they did not intend to analyze or share in generated reports.

Mitigation: Run the skill only on datasets approved for analysis and review generated report artifacts before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruiyongwang/skills/data-analysis-report)
- [Publisher profile](https://clawhub.ai/user/ruiyongwang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, chart files, HTML or PDF reports, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are optimized for Chinese-language output and local data processing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
