## Description: <br>
European Patent Office (EPO) patent intelligence and competitive analysis system for monitoring competitor patents, identifying technology trends, and generating strategic reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quratus](https://clawhub.ai/user/quratus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, R&D teams, and agent developers use this skill to collect EPO patent data, assess competitor activity, and produce strategic patent intelligence reports for manufacturing and technology monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports hard-coded tunnel credentials and scripts that can publish local reports to an external Cloudflare domain. <br>
Mitigation: Remove hard-coded Cloudflare credentials, verify who controls the target domain, and decide whether public report hosting is acceptable before running deployment scripts. <br>
Risk: The skill requires sensitive EPO API credentials. <br>
Mitigation: Provide EPO credentials through a managed secret mechanism and avoid committing or logging credential values. <br>
Risk: Cron and tunnel scripts can run with broad local authority. <br>
Mitigation: Run automation with least-privilege accounts, audit scheduled jobs before enabling them, and avoid running tunnel or cron scripts as root without review. <br>
Risk: Generated patent intelligence reports may influence business decisions. <br>
Mitigation: Review generated reports and strategic recommendations before relying on them for commercial decisions. <br>


## Reference(s): <br>
- [EPO OPS API Reference Documentation](references/EPO_API.md) <br>
- [Patent Analysis Patterns](references/ANALYSIS_PATTERNS.md) <br>
- [OpenClaw Agent Integration Guide](references/AGENT_INTEGRATION.md) <br>
- [Modern Dashboard & Report Framework Guidelines](references/REPORT_FRAMEWORKS.md) <br>
- [Report Generation Framework - Implementation Summary](references/REPORT_FRAMEWORK_SUMMARY.md) <br>
- [EPO Developer Portal](https://developers.epo.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, HTML reports] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python scripts, SQLite-backed patent data, and generated HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EPO API credentials and may use scheduled jobs, local databases, and report hosting scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
