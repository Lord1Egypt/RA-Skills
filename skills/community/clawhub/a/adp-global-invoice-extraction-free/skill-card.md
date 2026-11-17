## Description:

This skill helps agents call Laiye ADP's free public API to extract structured invoice and receipt data from PDFs, scanned files, images, and other supported document formats across more than 100 languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

Finance teams, agent users, and developers use this skill to submit authorized single-page invoice or receipt files by URL or base64 and receive structured extraction results for reimbursement, settlement, data entry, and workflow automation.

### Deployment Geography for Use:

Global, with separate Global and China public cloud endpoints

## Known Risks and Mitigations:

Risk: Invoices and receipts submitted through the skill are processed by Laiye-operated public cloud services.

Mitigation: Use only documents you are authorized to upload, avoid regulated or confidential records unless organizational policy permits it, and review Laiye privacy and retention terms before production use.

Risk: Free-tier and input limits can cause failed or rate-limited requests.

Mitigation: Check file size, page count, supported format, URL accessibility, and request volume before submission; handle documented 400 and 429 responses in downstream workflows.

Risk: Public file URL submission can expose documents beyond the agent workflow.

Mitigation: Prefer authorized short-lived HTTPS URLs or base64 upload paths, and do not use private network or internal IP URLs.

Risk: Automated extraction can produce incomplete or incorrect financial fields.

Mitigation: Review extracted invoice numbers, dates, parties, amounts, currency, tax fields, and line items before using results in accounting or payment workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/skills/adp-global-invoice-extraction-free)
- [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- [Laiye ADP Product Page](https://laiye.com/en/product/adp-platform)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON]

**Output Format:** [Markdown guidance with curl and Python examples plus JSON request and response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API requests provide either one public file URL or one base64-encoded file; the free tier supports single-page files under 2 MB with per-IP and global quotas.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
