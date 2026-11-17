## Description:

Accurate extraction of purchase order and sales order fields from PDFs, images, scanned copies, URLs, local files, and Base64 inputs through the Laiye ADP CLI, returning structured JSON for order-entry and supply-chain workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to invoke Laiye ADP for purchase order recognition, extract header and line-item fields, and integrate the resulting JSON into e-commerce, supply-chain, reconciliation, and warehouse-management systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions include curl-to-shell and PowerShell invoke-expression paths that create supply-chain risk.

Mitigation: Prefer npm or pinned, verified release artifacts; avoid pipe-to-shell installers and do not run installers with elevated privileges.

Risk: The skill sends purchase orders, invoices, IDs, or other sensitive documents to the Laiye ADP cloud service.

Mitigation: Confirm organizational approval for external document processing, use the appropriate regional ADP endpoint, and avoid submitting sensitive documents outside approved workflows.

Risk: Broad CLI documentation includes commands beyond purchase-order extraction.

Mitigation: Constrain agents to the order-extraction commands and use a scoped API key where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/skills/adp-purchase-order-recognition-and-extract)
- [Laiye ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [Laiye ADP China Mainland Portal](https://adp.laiye.com/?utm_source=clawhub)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [ADP OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd?from=from_copylink)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process single documents, batches, and asynchronous tasks; extracted order fields include header values and line-item tables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
