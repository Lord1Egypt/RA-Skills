## Description: <br>
Record daily work items into structured local Markdown logs and generate weekly, biweekly, or custom date range work reports from accumulated entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apple-sugar-xing](https://clawhub.ai/user/apple-sugar-xing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to capture daily work activities in local Markdown logs and turn them into structured weekly, biweekly, or custom date range reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local work-history files may retain sensitive project details. <br>
Mitigation: Avoid recording sensitive details that should not be retained, and periodically review or delete logs under ~/.workbuddy/work-logs/. <br>
Risk: Generated reports may contain confidential work information and are written into the workspace by default. <br>
Mitigation: Review generated reports before sharing and specify an appropriate output path when the current workspace is not suitable. <br>
Risk: Accidental activation could append unwanted work-log entries. <br>
Mitigation: Use explicit work-log or report-generation commands and review daily Markdown logs for unintended entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/apple-sugar-xing/skills/biweekly-work-report) <br>
- [Report Generation Template](references/report-template.md) <br>
- [Work Log Format Specification](references/work-log-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown files and inline Markdown text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local daily work-log files under ~/.workbuddy/work-logs/ and writes generated reports to the current workspace or a user-specified path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
