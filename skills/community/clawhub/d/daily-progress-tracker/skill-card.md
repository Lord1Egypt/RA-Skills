## Description: <br>
Helps users summarize daily work and generate structured daily reports when they ask for a daily report, work summary, or today report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yying01](https://clawhub.ai/user/yying01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill to turn daily work notes into a structured Markdown work report organized by project, status, next-day plans, and remarks. It can optionally save the report to a local reports folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The save script writes the current day's report to a predictable local Markdown file, and an existing file for today may be overwritten. <br>
Mitigation: Review the target folder before saving, set REPORTS_DIR to the intended private location, and keep backups when preserving multiple versions of the same day's report matters. <br>
Risk: Daily reports may include confidential project, meeting, blocker, or personnel details. <br>
Mitigation: Review report contents before saving or sharing, and store reports only in an access-controlled folder appropriate for the sensitivity of the work. <br>


## Reference(s): <br>
- [Daily Progress Tracker on ClawHub](https://clawhub.ai/yying01/daily-progress-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/yying01) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown daily report text, with an optional shell command that saves the report as a local Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled save script writes to ~/reports/YYYY-MM-DD.md by default or to REPORTS_DIR/YYYY-MM-DD.md when configured; no network access, credential use, or hidden behavior is reported by server security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
