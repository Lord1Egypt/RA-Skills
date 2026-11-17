## Description:

Convert PDF bank and credit card statements into clean transactions (JSON) or CSV, OFX, QFX, QBO and Xero CSV files with the BankConv API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wassim](https://clawhub.ai/user/wassim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and people handling bookkeeping use this skill to convert user-provided bank or credit card statement PDFs into transactions for analysis or files for accounting and spreadsheet software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial: four local references could not be matched to bundled files, so the benign verdict has medium confidence.

Mitigation: Review the unresolved references and the skill instructions in the context of intended use before installation.

Risk: Bank and credit card statements contain sensitive financial information and are uploaded to BankConv for conversion.

Mitigation: Upload only statements the user asked to convert, and explain that BankConv deletes them after 24 hours by default.

## Reference(s):

- [BankConv MCP integration](https://bankconv.com/integrations/mcp)
- [BankConv API documentation](https://bankconv.com/api-docs)

## Skill Output:

**Output Type(s):** [JSON, CSV, OFX, QFX, QBO, Xero CSV, Guidance]

**Output Format:** [Structured transaction data or downloadable accounting files, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF conversion uses account page credits; statement PDFs are uploaded to BankConv and deleted after 24 hours by default.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
