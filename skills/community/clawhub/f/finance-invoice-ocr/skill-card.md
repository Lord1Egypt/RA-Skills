## Description:

Provides an invoice OCR and accounting workflow for extracting invoice data from photos or screenshots, validating invoice details, classifying invoices, matching business records, and preparing ledger entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aolikeji](https://clawhub.ai/user/aolikeji)

### License/Terms of Use:

MIT-0

## Use Case:

Finance teams use this skill to turn invoice images or screenshots into structured invoice records, verification steps, accounting classifications, and ledger update guidance. It is intended for invoice processing workflows where OCR results and accounting entries remain subject to finance staff review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted invoice text from OCR may be written into spreadsheet cells and interpreted as formulas.

Mitigation: Sanitize spreadsheet cell values before writing OCR output, including formula-prefix characters, and preserve raw OCR data separately for audit review.

Risk: Incorrect OCR extraction or invoice classification could lead to inaccurate accounting entries.

Mitigation: Require explicit finance-staff confirmation before ledger updates and validate invoice numbers, dates, amounts, tax values, and buyer/seller identities.

Risk: Broad trigger phrases may activate the skill in unrelated finance or OCR contexts.

Mitigation: Narrow triggers to invoice-specific workflows and require the user to identify the intended invoice-processing action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aolikeji/skills/finance-invoice-ocr)
- [ClawHub metadata homepage](https://clawhub.ai/skills/finance-invoice-ocr)
- [Publisher profile](https://clawhub.ai/user/aolikeji)
- [National VAT invoice verification platform](https://inv-veri.chinatax.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with tables and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces invoice field schemas, verification workflows, ledger/table structures, sample spreadsheet-writing code, and accounting review guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
