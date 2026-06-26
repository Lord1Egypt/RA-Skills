## Description: <br>
Analyzes weekly or monthly code repository changes, generates code quality reports, and synchronizes analysis, review, commit, and statistics data to an internal code quality database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fightingdao](https://clawhub.ai/user/fightingdao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering managers use this skill to analyze weekly or monthly repository changes, score code quality, generate review findings, and sync reporting data for an internal dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite reporting data for a selected analysis period. <br>
Mitigation: Confirm the exact period, team, projects, database target, backup, and rollback plan before running synchronization. <br>
Risk: The skill can delegate code review to a secondary model for detailed analysis. <br>
Mitigation: Confirm that secondary-model review is allowed for the repository content before including sensitive code changes. <br>
Risk: The skill references notification channels and local notification scripts. <br>
Mitigation: Verify notification recipients, webhook or email configuration, and message content before sending reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fightingdao/fightingdao-code-quality-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with code blocks, SQL snippets, command examples, and structured review tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide database synchronization and notification steps through referenced local scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
