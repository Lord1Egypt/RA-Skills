## Description:

支持增值税专用发票、增值税普通发票、增值税电子发票、出租车票、火车票、飞机行程单、过路费发票、定额发票、客运汽车票、财政票据等30+常见国内票据类型的自动分类与全量字段抽取，输出结构化JSON，零配置开箱即用，适用于费用报销、财务记账、发票验真、差旅报销自动化等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external finance teams, and developers use this skill to classify Chinese invoices and receipts, extract structured fields, and receive invoice verification fields for reimbursement, accounting, tax-checking, and travel-expense automation workflows.

### Deployment Geography for Use:

China Mainland and overseas regions supported by Laiye ADP public cloud endpoints.

## Known Risks and Mitigations:

Risk: Install instructions include remote shell and PowerShell execution paths for ADP CLI setup.

Mitigation: Review the ADP CLI source or use a pinned, verified release, and avoid curl|bash and irm|iex installation commands.

Risk: The skill processes sensitive invoice and receipt data through Laiye ADP and may use a tax-verification service.

Mitigation: Confirm privacy, business, and compliance requirements before sending documents, and restrict the files or folders an agent may process.

Risk: ADP API credentials are required for extraction workflows.

Mitigation: Use a least-privilege API key and avoid exposing credentials to unauthorized users or logs.

## Reference(s):

- [Supported invoice types and fields](artifact/examples/supported-invoice-types.md)
- [VAT electronic invoice JSON example](artifact/examples/vat-electronic-invoice-new.json)
- [Laiye ADP China Mainland portal](https://adp.laiye.com/?utm_source=clawhub)
- [Laiye ADP Global portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases)
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [ADP Open API user guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying ADP extraction command returns structured JSON for single files, batches, and asynchronous task queries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
