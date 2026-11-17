## Description:

数据分析技能包 - 自动抓取、清洗、可视化、生成报告。适合数据分析师、运营人员，告别 Excel 手工操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdp6539](https://clawhub.ai/user/gdp6539)

### License/Terms of Use:

MIT

## Use Case:

External data analysts, operations staff, and business users use this skill to automate data collection, dataset cleaning, chart creation, and report generation from web, API, CSV, and JSON sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary marks the release suspicious because it overstates capabilities and includes under-scoped network, file-writing, and shell-execution behavior.

Mitigation: Review and constrain execution before installing; use dedicated input/output folders and run it only against trusted URLs and datasets.

Risk: Input sources, command arguments, or checked-in configuration can expose secrets or sensitive data.

Mitigation: Avoid passing secrets in command-line arguments or committed config files; use managed credentials and redact outputs before sharing reports.

Risk: PDF generation is specifically discouraged by the server security guidance until shell execution and filename validation are fixed.

Mitigation: Generate Markdown or HTML reports, or disable PDF output, until the publisher provides validation fixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gdp6539/skills/data-analysis-skill)
- [Publisher profile](https://clawhub.ai/user/gdp6539)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated CSV, SVG, HTML, Markdown, or PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch data from URLs or APIs and write generated datasets, charts, and reports to local output paths.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
