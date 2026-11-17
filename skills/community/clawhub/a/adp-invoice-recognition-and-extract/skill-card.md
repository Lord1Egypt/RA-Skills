## Description:

Multi-language, multi-currency invoice recognition and extraction that helps agents use Laiye ADP to extract invoice numbers, dates, supplier and buyer details, currency, tax, totals, and line items as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, finance teams, and developers use this skill to process invoices, receipts, bills, and vouchers through Laiye ADP and return normalized invoice fields for accounts payable automation, expense reimbursement, and cross-border trade workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends shell and PowerShell remote script installers.

Mitigation: Prefer npm installation or a pinned release artifact, and verify the package or binary before installation.

Risk: Invoice and document contents are sent to Laiye ADP's cloud service.

Mitigation: Use the skill only with approved documents, confirm data handling requirements, and configure a least-privilege API key.

Risk: The artifact describes broader ADP capabilities beyond invoice extraction, including batch processing, URL-list processing, and custom-app management.

Mitigation: Keep routine use scoped to invoice extraction and require explicit user approval before batch folders, URL-list processing, or custom-app management commands.

Risk: License evidence is inconsistent between server metadata and artifact/license.md.

Mitigation: Confirm the authoritative license or commercial authorization terms before public release or commercial deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/skills/adp-invoice-recognition-and-extract)
- [Laiye ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [Laiye ADP China Mainland Portal](https://adp.laiye.com/?utm_source=clawhub)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- [ADP CLI GitHub Releases](https://github.com/laiye-ai/adp-cli/releases)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ADP API credentials and sends invoice or document contents to Laiye ADP's cloud service.]

## Skill Version(s):

1.0.2 (source: server release metadata, created 2026-05-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
