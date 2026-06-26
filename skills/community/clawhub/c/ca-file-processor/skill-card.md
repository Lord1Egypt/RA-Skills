## Description: <br>
Processes PDF, Excel, CSV, JPG, and PNG financial documents for Indian CA firms, extracting text, tables, and fields such as GSTIN, invoice numbers, totals, and dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[purvik6062](https://clawhub.ai/user/purvik6062) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External accounting and tax professionals can use this skill to route uploaded financial files to local processors, extract document text and structured fields, and prepare summaries or follow-up questions for review. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive financial documents may be included in model context or logs. <br>
Mitigation: Use the skill only on explicitly selected files and avoid payroll, tax IDs, bank details, or client records unless that exposure is acceptable. <br>
Risk: Broad file handling may process unrelated attachments. <br>
Mitigation: Limit invocation to user-selected PDF, Excel, CSV, JPG, JPEG, and PNG files that are intended for document extraction. <br>
Risk: OCR and heuristic extraction can misread numbers or fields in low-quality scans. <br>
Mitigation: Treat low-confidence OCR and extracted numeric fields as draft results and ask the user to confirm them before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/purvik6062/ca-file-processor) <br>
- [Publisher profile](https://clawhub.ai/user/purvik6062) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON dictionaries from local processor scripts, with extracted text, tables, fields, summaries, confidence notes, and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports PDF, XLSX, XLS, CSV, JPG, JPEG, and PNG inputs; CSV rows and spreadsheet rows are capped, and OCR results may require human review.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
