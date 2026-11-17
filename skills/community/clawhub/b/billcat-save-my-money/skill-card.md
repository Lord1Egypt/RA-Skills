## Description:

使用 BillCat API 从自然语言中提取并保存记账信息到乖猫记账 App，并支持删除账单、账单统计、账本与资产列表查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[isee15](https://clawhub.ai/user/isee15)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Chinese natural-language expense or income descriptions into BillCat records, delete records by billId, and summarize income, expenses, books, and assets over date ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create financial records remotely from natural-language input.

Mitigation: Review the extracted bill details before using the saved record for accounting or reporting.

Risk: The skill can delete one or multiple bill records by billId without a second confirmation step.

Mitigation: Confirm billIds and keep the original saved bill output before running delete operations.

Risk: Bill descriptions, date ranges, and the BillCat API key are sent to billcat.cn.

Mitigation: Install only if the user trusts BillCat and is comfortable sharing those inputs with the BillCat service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/isee15/skills/billcat-save-my-money)
- [Declared skill homepage](https://github.com/isee15/billcat-save-my-money)
- [BillCat extract bill API endpoint](https://billcat.cn/api/app/openclaw/extractbill)
- [BillCat skill API endpoint](https://billcat.cn/api/app/openclaw/skill)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON, formatted JSON, or concise Markdown from command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BILLCAT_API_KEY and sends user-provided bill descriptions or date ranges to BillCat endpoints.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
