## Description: <br>
广告投放数据分析 skill that analyzes uploaded Excel or CSV advertising reports, dynamically identifies columns, summarizes metrics, detects anomalies, generates visual charts, and provides optimization suggestions for exported reports from major ad platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ming0429](https://clawhub.ai/user/ming0429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to process local advertising spreadsheet exports, generate summary statistics and PNG charts, and receive optimization suggestions based on detected dimensions and metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or unrelated spreadsheet data may be processed when a broad analysis request includes the wrong attachment. <br>
Mitigation: Use only advertising report files intended for local processing and confirm file relevance before running the analyzer. <br>
Risk: Optimization suggestions are generated from detected spreadsheet columns and statistical summaries, so they may miss business context. <br>
Mitigation: Review the generated report and charts against campaign goals before changing budgets or pausing campaigns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ming0429/ad-analyzer-yima) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, analysis] <br>
**Output Format:** [Markdown guidance with shell commands and local script output; the analyzer writes PNG chart files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus pandas, openpyxl, xlrd, matplotlib, and seaborn; processes spreadsheet files locally.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
