## Description: <br>
帮用户快速记录日常支出和收入到飞书多维表格。支持文字记账和图片小票 OCR 解析。首次使用时会学习用户已有的记账本习惯，或引导新建记账本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haojie0114-lang](https://clawhub.ai/user/haojie0114-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams who track personal or small-team finances use this skill to record income and expenses in Feishu Bitable from natural-language entries or receipt images. It can learn an existing table structure or guide setup of a new bookkeeping table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive financial records, table identifiers, and receipt images. <br>
Mitigation: Install only for Feishu tables you trust the skill to access, and protect or delete local configuration files that contain bookkeeping metadata. <br>
Risk: OCR or natural-language parsing can produce incorrect amounts, categories, or receipt line items. <br>
Mitigation: Review parsed entries before batch writing receipts and confirm the target table during setup. <br>


## Reference(s): <br>
- [AccountingOnFeishu on ClawHub](https://clawhub.ai/haojie0114-lang/accountingonfeishu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration] <br>
**Output Format:** [Conversational text with Feishu Bitable record creation requests and local configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu Bitable records and local bookkeeping configuration based on user-provided table access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
