## Description: <br>
Guides agents through understanding, cleaning, exploring, and reporting on datasets while keeping data quality issues and user objectives explicit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoM0](https://clawhub.ai/user/zhaoM0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and data-focused agents use this skill to inspect uploaded datasets, assess data quality, plan cleaning steps, and summarize analysis results in clear business language. It is especially oriented toward CSV, Excel, and general tabular data exploration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad dataset-related triggers and may activate on brief or ambiguous data requests. <br>
Mitigation: Confirm the user's analysis goal and data context before performing substantial cleaning, transformation, or reporting work. <br>
Risk: Uploaded datasets may contain sensitive or confidential information. <br>
Mitigation: Avoid uploading sensitive files unless processing is intended, and review proposed cleaning or transformation steps before applying them. <br>
Risk: Data cleaning choices can change analysis results or remove important records. <br>
Mitigation: Keep original data unchanged, document each transformation, and ask for user confirmation before handling ambiguous or high-impact quality issues. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaoM0/famou-data-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/zhaoM0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and guidance, often with code or shell command snippets for data inspection and processing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce data quality summaries, cleaning plans, analysis reports, processing records, and recommendations for follow-up analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
