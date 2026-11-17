## Description:

账单伙伴记录个人和家庭日常收支、管理固定支出，并生成月度汇总报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiss1952](https://clawhub.ai/user/kiss1952)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain local personal or household bookkeeping records from natural-language expense, income, fixed-cost, and monthly-summary requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal financial records are stored in the workspace and may be visible to anyone with workspace access.

Mitigation: Use the skill only in a private workspace and periodically review the generated finance-records/ files.

Risk: Natural-language parsing can misclassify transactions or record an incorrect amount, merchant, date, or category.

Mitigation: Ask for confirmation when transaction details are uncertain and review monthly summaries before relying on them.

## Reference(s):

- [Data Schema](artifact/references/data-schema.md)
- [Expense Categories](artifact/references/categories.md)
- [Fixed-Cost Rules](artifact/references/fixed-costs.md)
- [ClawHub Skill Page](https://clawhub.ai/kiss1952/skills/buddy-bills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Natural-language responses plus structured YAML bookkeeping files and monthly markdown-style summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and updates records locally under finance-records/ in the active workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
