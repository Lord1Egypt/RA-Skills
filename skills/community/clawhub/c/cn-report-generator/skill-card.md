## Description: <br>
Generates Chinese daily, weekly, and monthly work report drafts from local memory and daily log files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to turn local OpenClaw memory and daily work logs into structured Chinese daily and weekly report drafts. It is intended for personal productivity reporting where the user reviews generated Markdown before sharing it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include sensitive work details from local OpenClaw memory and work-log files. <br>
Mitigation: Review generated reports before sharing them outside the intended audience. <br>
Risk: Rerunning a daily or weekly report can replace the existing Markdown file for that date or week. <br>
Mitigation: Keep backups or review the target report path before rerunning generation for an existing period. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-report-generator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown report files and concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved locally under ~/reports for daily and weekly outputs; monthly output is documented but the bundled script reports it as still in development.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
