## Description:

审计定时任务的月度 token 消耗，并评估任务合并、降频与冗余清理方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT-0

## Use Case:

面向使用 WorkBuddy 定时任务的用户，汇总上月 token 消耗并生成任务合并、降频和冗余任务审计建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions allow deletion of tasks judged to be replaced without explicit user approval.

Mitigation: Use an initial read-only audit, save original task configurations, and require explicit approval for every task change or deletion.

Risk: The instructions and report script require unrelated promotional content in generated reports.

Mitigation: Remove mandatory advertising from the instructions and script before using or distributing the skill.

## Reference(s):

- [ClawHub release](https://clawhub.ai/guipi888/skills/automation-token-optimizer)
- [Publisher GitHub profile](https://github.com/guipi888)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown report with tables and optimization recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monthly token-usage summaries and proposed task changes; verify the recommendations against your environment.]

## Skill Version(s):

2.0.1 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
