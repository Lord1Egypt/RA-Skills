## Description:

A universal document parsing skill powered by Laiye ADP that parses PDFs, images, scanned documents, and Office files into key fields and structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

Developers and business automation teams use this skill to configure the Laiye ADP CLI and parse local, URL, Base64, batch, or async documents into structured JSON for storage, retrieval, data pipelines, quality inspection, and system integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions include unpinned global CLI installation and remote script execution.

Mitigation: Review before installing, prefer a pinned package or signed release, avoid curl-to-shell and PowerShell pipe execution, and require explicit approval before an agent installs or updates the CLI.

Risk: Document parsing sends user documents to Laiye ADP's cloud service.

Mitigation: Submit only documents approved for that service, especially for invoices, IDs, contracts, or regulated data.

Risk: The skill requires ADP API credentials.

Mitigation: Keep API keys out of prompts and logs, use approved secret storage or environment variables, and clear local configuration when access is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/adp-pdf-to-structured-json)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- [Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- [Laiye ADP website](https://laiye.com/en/product/adp-platform)
- [ADP Global portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP Mainland China portal](https://adp.laiye.com/?utm_source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands; ADP parsing commands return structured JSON or exported JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local files, URLs, Base64 input, batch folders, async task queries, and exported per-file JSON results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
