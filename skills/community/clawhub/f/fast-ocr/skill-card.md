## Description:

FastOCR helps agents perform local OCR on receipt, invoice, and ticket images and return extracted text plus structured fields for supported document types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaojiren](https://clawhub.ai/user/gaojiren)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, operations, travel, and administrative users can use this skill to extract text and key fields from invoices, tickets, receipts, screenshots, and scanned documents. It is especially oriented toward local processing of financial, tax, medical, and travel records where extracted output should be handled as confidential.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Offline and no-network claims conflict with an unpinned OCR dependency and a first-run model download.

Mitigation: Review the dependency before installation, pin the OCR package version, and verify or pre-cache model artifacts before using the skill in sensitive environments.

Risk: The skill may process financial, tax, medical, or travel records that contain confidential information.

Mitigation: Only process documents intended for OCR, handle extracted text as confidential, and apply appropriate retention and access controls.

Risk: OCR extraction can be incomplete or inaccurate when images are blurred, poorly lit, obstructed, or contain unsupported handwriting.

Mitigation: Use clear source images and manually verify important extracted fields before relying on the output for reimbursement, tax, medical, or travel workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaojiren/skills/fast-ocr)
- [FastOCR documentation](https://docs.openclaw.ai/skills/fast-ocr)
- [OpenClaw repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-like OCR extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR quality depends on image clarity, lighting, document condition, and model availability.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
