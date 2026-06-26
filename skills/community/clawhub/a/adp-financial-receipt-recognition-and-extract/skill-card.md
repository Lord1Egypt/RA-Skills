## Description: <br>
Supports automatic classification, field extraction, and verification for 30+ common financial invoices and receipts in China, returning structured JSON through Laiye ADP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Finance, operations, and developer teams use this skill to route invoices, receipts, and travel documents through the ADP CLI for extraction, classification, and invoice verification workflows. It is suited to expense reimbursement, bookkeeping, invoice authenticity checks, and AP automation where external cloud processing is approved. <br>

### Deployment Geography for Use: <br>
China-focused; ADP documents China mainland and overseas service endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: Invoices, receipts, and extracted tax fields may contain sensitive financial or personal data and are processed through Laiye ADP cloud services and, for supported invoices, the tax verification platform. <br>
Mitigation: Install and use the skill only when organizational policy allows this external processing; submit only approved documents and minimize broad folder processing. <br>
Risk: The skill requires ADP credentials for cloud API access. <br>
Mitigation: Use a least-privilege ADP API key, keep credentials out of prompts and logs, and rotate or revoke keys according to organizational policy. <br>
Risk: The artifact includes pipe-to-shell installation options and broad CLI processing examples. <br>
Mitigation: Prefer npm or verified release downloads, review install scripts before use, and scope batch commands to approved directories only. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/adp-financial-receipt-recognition-and-extract) <br>
- [Laiye ADP Official Website](https://laiye.com/en/product/agentic-document-processing) <br>
- [ADP China Mainland Portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh) <br>
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd?from=from_copylink) <br>
- [Supported Invoice Types](examples/supported-invoice-types.md) <br>
- [VAT Electronic Invoice Example](examples/vat-electronic-invoice-new.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; ADP CLI results are structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local files, URLs, Base64 inputs, directories, asynchronous tasks, and exported batch result files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
