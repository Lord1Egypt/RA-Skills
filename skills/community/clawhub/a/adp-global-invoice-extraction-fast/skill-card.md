## Description:

High-performance API for global invoice recognition. Each page is parsed in 5 seconds with reliable high-concurrency support. It extracts full invoice data and returns structured JSON directly, ideal for financial automation and cross-border document processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

Enterprise finance teams, system integrators, and developers use this skill to configure Laiye ADP document extraction workflows for invoices, receipts, and billing documents. The skill guides agents through CLI setup, app discovery, extraction commands, async or batch processing, and JSON result handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include unpinned remote installer execution and global package installation.

Mitigation: Use a pinned, verified release or reviewed binary, and avoid administrator or root privileges for npm and installer commands.

Risk: Invoice, receipt, and billing documents may contain confidential or regulated financial data sent to a cloud service.

Mitigation: Confirm organizational approval and data-handling requirements before using the skill, especially for regulated or confidential documents.

Risk: The ADP API key is a secret used to access the cloud service.

Mitigation: Store the API key in approved secret storage or environment configuration and do not expose it in logs, prompts, shared files, or tickets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/adp-global-invoice-extraction-fast)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- [ADP Product Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases)
- [Laiye ADP product page](https://laiye.com/en/product/adp-platform)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The ADP service returns structured JSON extraction results and may write per-document JSON files for batch exports.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
