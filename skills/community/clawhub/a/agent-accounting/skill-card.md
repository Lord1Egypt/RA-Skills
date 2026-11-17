## Description:

Agent Accounting helps accounting agents process invoices, generate bookkeeping vouchers and financial reports, calculate taxes, run tax-risk checks, prepare filing payloads, and produce an HTML dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External accounting agencies and developers use this skill to automate recurring bookkeeping workflows for small and midsize business clients, including invoice OCR, voucher creation, reporting, tax calculation, filing preparation, and review of tax-risk indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive invoice and tax data may be sent to cloud OCR or third-party filing services.

Mitigation: Use demo or simulation mode by default; only enable external services after confirming data-sharing terms, credentials, endpoint ownership, and HTTPS-only transport.

Risk: Live tax submissions could be sent to an unreviewed or misconfigured destination.

Mitigation: Allowlist filing destinations and confirm TAX_API_BASE_URL immediately before any production submission.

Risk: Cached OCR access tokens may expose credentials or service access if the local environment is shared.

Mitigation: Protect the token cache location, restrict local file permissions, or disable token caching in sensitive deployments.

Risk: Generated dashboard reports may include untrusted OCR or invoice fields.

Mitigation: Fix and verify HTML escaping before opening dashboards generated from untrusted source documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/agent-accounting)
- [Source Repository](https://github.com/bettermen/agent-accounting)
- [Baidu Finance OCR](https://ai.baidu.com/tech/ocr/finance)
- [Baidu OCR API Documentation](https://ai.baidu.com/ai-doc/OCR/Zk3h7xz52)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated JSON/XML-like tax data, and HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call optional external OCR and tax filing services when credentials and endpoints are configured.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
