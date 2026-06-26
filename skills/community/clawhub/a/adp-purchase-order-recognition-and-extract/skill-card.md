## Description: <br>
Accurate extraction of all fields from purchase orders and sales orders in various formats, including PO number, order date, parties, addresses, currency, total amount, and line items, with structured JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Developers, operations teams, and business users use this skill to run Laiye ADP purchase-order extraction from local files, URLs, Base64 inputs, folders, or async tasks. It supports order entry, supply-chain reconciliation, warehouse workflows, and downstream automation that consumes structured JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends order documents to Laiye ADP as a cloud processor and requires a locally configured ADP API key. <br>
Mitigation: Use only approved documents, protect the API key with local secret-handling practices, and avoid sharing credentials in prompts, logs, or exported files. <br>
Risk: Installer examples include pipe-to-shell commands for shell and PowerShell. <br>
Mitigation: Prefer npm or reviewed release binaries, and inspect any installer script before execution. <br>
Risk: Packaged instructions expose broader document-processing and custom-app administration capabilities than purchase-order extraction requires. <br>
Mitigation: Limit agent use to the built-in order extraction app and avoid custom-app management or general document parsing unless explicitly intended. <br>
Risk: Extraction and batch processing can consume paid ADP service credits. <br>
Mitigation: Check credit balance, confirm large batch jobs before running them, and monitor usage against account limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/adp-purchase-order-recognition-and-extract) <br>
- [ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP China Mainland Portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh) <br>
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd?from=from_copylink) <br>
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe) <br>
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with CLI commands; ADP extraction results are structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ADP API key and an order extraction app ID; batch and async workflows may write JSON result files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
