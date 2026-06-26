## Description: <br>
一个简单的日常开销记录和统计工具，帮助管理个人财务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangjinghua0127](https://clawhub.ai/user/yangjinghua0127) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to record simple personal expenses, view recent bills, summarize spending by category or month, and export local JSON reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes personal expense records to local JSON files. <br>
Mitigation: Use it only in a workspace where local expense data can be stored, backed up, and reviewed before sharing artifacts. <br>
Risk: ClawScan guidance recommends care with local-authority workflow helpers even though this release was rated clean. <br>
Mitigation: Review commands and generated files before deployment, and follow the documented confirmation steps for any sensitive local action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangjinghua0127/expense-note) <br>
- [Publisher profile](https://clawhub.ai/user/yangjinghua0127) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON files, guidance] <br>
**Output Format:** [Console text and local JSON expense data or report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON persistence under data/expenses.json and can export dated report JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
