## Description:

Data Analysis helps agents analyze datasets, summarize CSV files, create charts, build dashboards, and prepare KPI, funnel, retention, financial, and revenue analyses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logictortoise](https://clawhub.ai/user/logictortoise)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to delegate data analysis and visualization requests to the AnyGen CLI, including sales analysis, financial modeling, cohort analysis, funnel analysis, KPI reports, retention analysis, conversion analysis, CSV summarization, and dashboard creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis data may be sent to AnyGen's servers.

Mitigation: Use only with approved datasets and avoid sensitive business, financial, personal, or regulated data unless organizational review allows it.

Risk: The workflow uses API credentials through ANYGEN_API_KEY or CLI authentication.

Mitigation: Prefer browser-based login or managed environment variables, avoid pasting API keys into shell history, and rotate credentials if exposure is suspected.

Risk: The skill installs and relies on mutable third-party components, including @anygen/cli and a companion workflow skill.

Mitigation: Review and pin the CLI and companion skill versions before deployment, and repeat security review when dependencies change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/logictortoise/skills/anygen-data-analysis)
- [Publisher profile](https://clawhub.ai/user/logictortoise)
- [AnyGen website](https://www.anygen.io)
- [AnyGen CLI package](https://www.npmjs.com/package/@anygen/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on the AnyGen CLI, the ANYGEN_API_KEY environment variable, browser-based login, and the companion anygen-workflow-generate skill.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
