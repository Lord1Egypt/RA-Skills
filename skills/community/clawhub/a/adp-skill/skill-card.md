## Description:

Enterprise-grade agentic document processing API. Accurately extracts key fields and line items from invoices, receipts, orders and more across 10+ file formats, with confidence scoring. Zero-configuration, fast integration. Professionally optimized on massive enterprise documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anna4lucky-stack](https://clawhub.ai/user/anna4lucky-stack)

### License/Terms of Use:

Commercial License Required

## Use Case:

Developers and enterprise teams use this skill to integrate Laiye ADP document extraction into agent workflows for invoices, receipts, purchase orders, financial documents, logistics documents, and multi-table data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business documents may be sent to Laiye's external ADP service for processing.

Mitigation: Confirm organizational approval, retention terms, deletion terms, and privacy requirements before uploading invoices, receipts, purchase orders, or other sensitive documents.

Risk: API credentials are required for access to the external service.

Mitigation: Use scoped credentials where available, store keys in environment variables or a secret store, avoid committing credentials, and rotate keys regularly.

Risk: Extracted fields can include low-confidence or incorrect values.

Mitigation: Review fields with low confidence before using extracted data in financial, logistics, or business decision workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anna4lucky-stack/skills/adp-skill)
- [ADP Portal and API Base URL](https://adp-global.laiye.com/)
- [Complete API Documentation](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API request examples, response schemas, credential environment variables, file handling limits, and operational safeguards.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
