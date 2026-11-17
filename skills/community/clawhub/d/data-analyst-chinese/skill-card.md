## Description:

数据分析师 helps agents generate Python-based workflows for data cleaning, statistical analysis, time-series analysis, visualization, and structured analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, data analysts, product managers, operations teams, developers, and engineers use this skill to inspect datasets, generate Pandas analysis code, create visualizations, and draft analysis reports. It is not intended for real-time streaming data processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read, write, and execute code in the local working environment.

Mitigation: Use it only with datasets and directories intended for analysis, and review generated Python or shell commands before execution.

Risk: Data analysis outputs may be incorrect or misleading if the source data, statistical method, or visualization choice is unsuitable.

Mitigation: Validate generated statistics and reports against business context, dataset quality, and the intended analysis method.

Risk: Sensitive datasets could be exposed through generated code, reports, logs, or API usage.

Mitigation: Limit access to sensitive files, avoid unnecessary external API calls, and sanitize outputs before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/data-analyst-chinese)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Configuration instructions, Markdown, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local file operations or executable analysis code that should be reviewed before use with sensitive datasets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
