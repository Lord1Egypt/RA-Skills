## Description: <br>
FastOCR is an offline OCR skill for extracting text and structured fields from invoices, train tickets, air tickets, taxi receipts, and other business documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaojiren](https://clawhub.ai/user/gaojiren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, operations, travel, and administrative users use this skill to extract OCR text and structured receipt or ticket fields for reimbursement, ticket management, document digitization, and batch processing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR inputs and extracted text may contain sensitive financial, medical, travel, or identity information. <br>
Mitigation: Process only documents appropriate for the current agent environment, avoid unnecessary retention or logging, and handle extracted text as sensitive data. <br>
Risk: OCR output may be incomplete or incorrect for low-quality images, complex layouts, or compliance-critical fields. <br>
Mitigation: Review extracted fields before reimbursement, accounting, legal, medical, or compliance use. <br>
Risk: The OCR dependency or first-run model download can affect supply-chain trust in business workflows. <br>
Mitigation: Pin and verify the rapidocr-onnxruntime dependency and model source before deployment in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaojiren/fast-ocr) <br>
- [FastOCR documentation](https://docs.openclaw.ai/skills/fast-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text and JSON-like structured OCR results with Markdown usage guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sensitive document text and confidence scores; important financial or compliance fields should be reviewed by a human.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
