## Description: <br>
使用 BillCat API 从自然语言中提取并保存记账信息到乖猫记账 App，并支持删除账单、账单统计、账本与资产列表查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isee15](https://clawhub.ai/user/isee15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Chinese natural-language expense or income descriptions into saved BillCat records, retrieve bill IDs, delete records by billId, and summarize income, expenses, books, and assets over a date range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a BillCat API key that grants access to account operations. <br>
Mitigation: Store BILLCAT_API_KEY only in environment or local OpenClaw configuration files, and do not commit or log the secret. <br>
Risk: The skill can save new financial records and may create duplicates during testing or repeated runs. <br>
Mitigation: Review extracted bill results before relying on them, and avoid repeatedly submitting the same bill text unless duplicate entries are intended. <br>
Risk: The delete command can remove real BillCat records by billId. <br>
Mitigation: Double-check bill IDs before deletion and prefer Markdown or pretty JSON output when saving bills so the returned billId is visible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/isee15/billcat-save-my-money) <br>
- [BillCat extractbill API endpoint](https://billcat.cn/api/app/openclaw/extractbill) <br>
- [BillCat skill API endpoint](https://billcat.cn/api/app/openclaw/skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown emitted by Python command-line scripts, with configuration guidance for API key setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BILLCAT_API_KEY; commands can save or delete real BillCat financial records.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
