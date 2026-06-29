## Description: <br>
Activity Duration Estimation helps agents plan projects by creating WBS breakdowns, estimating durations with PERT and Monte Carlo methods, generating project documents, and producing economic and earned-value analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Project managers, analysts, and delivery teams use this skill to decompose project scope, estimate activity durations, generate planning documents, and evaluate financial or earned-value performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags broad local database access, including reading, importing, and exporting SQLite knowledge bases. <br>
Mitigation: Use the skill only with project data and database paths you intend to expose, and review generated or imported knowledge-base content before relying on it. <br>
Risk: The security review notes an unauthenticated settings server. <br>
Mitigation: Run the settings server only in a trusted local environment and avoid exposing it on untrusted networks. <br>
Risk: Generated economic and EVM HTML reports may load Chart.js from a CDN. <br>
Mitigation: Treat generated reports as network-loading pages and review them before opening or sharing in restricted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/activity-duration-estimation) <br>
- [Methods](references/methods.md) <br>
- [WBS Methodology](references/wbs-methodology.md) <br>
- [Project Docs Methodology](references/project-docs-methodology.md) <br>
- [Economic Analysis Methodology](references/economic-analysis-methodology.md) <br>
- [EVM Methodology](references/evm-methodology.md) <br>
- [Report Template](references/report-template.md) <br>
- [Permissions](references/permissions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with generated self-contained HTML reports and project document templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local SQLite knowledge bases and configurable settings for search, knowledge-base use, document mode, and report generation.] <br>

## Skill Version(s): <br>
1.11.7 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
