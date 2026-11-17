## Description:

Analyze weekly attendance records for employees at Zhuihui Branch from XLSX data and prepare attendance report outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang2y](https://clawhub.ai/user/wang2y)

### License/Terms of Use:

MIT-0

## Use Case:

Branch operations and administrative users use this skill to analyze Zhuihui Branch weekly attendance spreadsheets, apply branch-specific schedule rules, and produce report-ready attendance metrics.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The advertised DOCX/XLSX report outputs do not match the bundled script, which writes JSON attendance analysis.

Mitigation: Confirm expected deliverables before use and verify or add a rendering step when DOCX reports or XLSX supplements are required.

Risk: Attendance records can contain sensitive employee information.

Mitigation: Review data handling requirements before installing or running the skill, and keep generated JSON, DOCX, or XLSX files in approved storage.

Risk: Dependency installation from an unpinned or untrusted source can introduce supply-chain variance.

Mitigation: Install dependencies from a pinned requirements file or a trusted internal package source.

## Reference(s):

- [Special Attendance Analysis Rules](artifact/references/special-attendance-analysis-rules.md)
- [Example Weekly Attendance Analysis](artifact/examples/example-usage.md)
- [ClawHub Skill Release](https://clawhub.ai/wang2y/skills/analyzing-attendance-record-zhzh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON attendance analysis output; artifact documentation also describes DOCX and XLSX report deliverables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XLSX attendance input with the documented Zhuihui Branch column structure. Confirm the desired final report artifacts because the bundled script writes JSON analysis data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
