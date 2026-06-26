## Description: <br>
Analyzes any CSV file and returns row count, column names, and basic statistics for numeric columns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[democ4s](https://clawhub.ai/user/democ4s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other ClawHub users use this skill to inspect CSV files and quickly summarize row count, column names, and numeric min, max, and average values without modifying the source file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided CSV files, which may contain sensitive or confidential data. <br>
Mitigation: Review the CSV path before running the skill and avoid providing secrets or sensitive files unless the analysis is intended. <br>
Risk: CSV parsing or inferred numeric types may produce incomplete or misleading summary statistics for malformed data. <br>
Mitigation: Review the source CSV and treat generated statistics as a quick inspection aid rather than a validated data-quality report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/democ4s/c4s-csv-stats-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Shell commands] <br>
**Output Format:** [Markdown-formatted text with CSV row, column, and numeric summary statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and pandas; reads a user-provided CSV path and does not modify the original CSV file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
