## Description: <br>
数据分析与反馈技能 - 投放效果数据采集、分析与模型迭代建议 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JEyeshield](https://clawhub.ai/user/JEyeshield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators and developers use this skill to collect ad performance data, calculate campaign and material metrics, generate reports, and receive optimization feedback for model or creative iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign performance data may appear in reports, events, and logs. <br>
Mitigation: Use only analytics data that is appropriate for the OpenClaw runtime and verify who can access logs, emitted events, and generated reports. <br>
Risk: Unnecessary personal or sensitive data could be included in analytics inputs or exported reports. <br>
Mitigation: Limit inputs to the minimum campaign and material metrics needed for the analysis, and avoid adding personal data unless explicitly required and approved. <br>
Risk: CSV exports may be unsafe to open in spreadsheets when material IDs are not formula-neutralized. <br>
Mitigation: Review or sanitize CSV exports before opening them in spreadsheet tools, especially when material IDs can be user-controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JEyeshield/ad-production-analytics-feedback) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, CSV, Guidance] <br>
**Output Format:** [JSON command responses, text feedback, and CSV report strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes aggregated ad performance metrics, report IDs, feedback suggestions, alerts, and CSV exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
