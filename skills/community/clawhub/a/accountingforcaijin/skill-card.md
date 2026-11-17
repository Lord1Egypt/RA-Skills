## Description:

智能记账助手，用于在用户提到账本、流水、收支、应收应付、发票、票据或报销时，从文字或预处理后的多媒体内容生成和查询记账操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[heygallon](https://clawhub.ai/user/heygallon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record and query income, expenses, receivables, payables, ledgers, accounts, categories, handlers, and companies through a Caiwu accounting service. It supports direct text bookkeeping and bookkeeping after OCR, speech-to-text, or file parsing by companion skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create financial records from inferred or defaulted data.

Mitigation: Require the agent to show the normalized transaction and get explicit approval before every add operation.

Risk: OCR, speech, file, batch, or defaulted fields may produce inaccurate accounting entries.

Mitigation: Review extracted amount, transaction type, ledger, category, dates, invoice status, and due date before execution.

Risk: Local JSON file paths passed as command arguments may cause file contents to be sent to the accounting API.

Mitigation: Pass inline JSON unless file upload is intended, and avoid sensitive local file paths.

Risk: The skill depends on a remote accounting service and an API token.

Mitigation: Install only when the service is trusted and the token can be scoped, rotated, or revoked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heygallon/skills/accountingforcaijin)
- [Caiwu accounting API base URL](https://api.caiwu888.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ACCOUNTING_API_TOKEN and Python; add, query, ledger, account, category, handler, and company commands exchange JSON with the remote accounting API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
