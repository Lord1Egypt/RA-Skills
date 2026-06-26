## Description: <br>
Automated data reporting and dashboard generation. Connect to databases, APIs, spreadsheets. Generate PDF/PPT/Excel reports with charts. Schedule daily/weekly/monthly reports. Send via email, Slack, Teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fuczy](https://clawhub.ai/user/Fuczy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business teams, analysts, and operators use this skill to define recurring reports that pull data from databases, SaaS APIs, spreadsheets, and files, then produce dashboards, spreadsheets, slide decks, PDFs, alerts, and team notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports automated access to sensitive business data and recurring distribution through email, chat, shared documents, or public dashboards. <br>
Mitigation: Use read-only, least-privilege credentials; keep secrets out of report YAML; verify every recipient, channel, shared document, and public dashboard setting before enabling schedules. <br>
Risk: Recurring reports and public URLs can continue sharing stale, confidential, or unintended data after initial setup. <br>
Mitigation: Test with sample or sanitized data first, avoid public URLs unless the data is intentionally public, and confirm how scheduled jobs can be paused and removed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Fuczy/clawd-data-reporter) <br>
- [Publisher Profile](https://clawhub.ai/user/Fuczy) <br>
- [Skill Homepage](https://clawhub.com/skills/data-reporter) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe scheduled report definitions, connector settings, generated report files, dashboards, notifications, and alerting workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
