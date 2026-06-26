## Description: <br>
Extracts mutual fund monthly report data from PDFs with text and OCR, compares two months, and fills an Excel template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imkiiki](https://clawhub.ai/user/imkiiki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operations teams use this skill to extract values from fund monthly report PDFs, compare prior and current month data, and produce a populated Excel workbook while preserving the template structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process broad local folders and write generated financial spreadsheets. <br>
Mitigation: Run it only on narrow, trusted folders and confirm the PDF inputs, Excel template, and output path before execution. <br>
Risk: The artifact includes ZIP handling and auto-start style usage instructions that may process unintended files if inputs are not trusted. <br>
Mitigation: Avoid ZIP inputs unless the archive is trusted, inspect extracted contents first, and do not run scripts automatically without reviewing the command arguments. <br>
Risk: OCR and PDF extraction can produce incorrect financial values. <br>
Mitigation: Review generated spreadsheets against the source PDFs before using the results for reporting or business decisions. <br>
Risk: Dependency installation may require elevated privileges for Tesseract, Poppler, and Python packages. <br>
Mitigation: Prefer a virtual environment for Python packages and have a system administrator install system OCR dependencies when elevated privileges are needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imkiiki/fundreport-scrape) <br>
- [OCR rules](references/ocr_rules.md) <br>
- [Field mapping rules](references/field_mapping.md) <br>
- [Template learning rules](references/template_learning.md) <br>
- [Batch processing rules](references/batch_processing.md) <br>
- [Extraction templates](references/extraction_templates.json) <br>
- [Interaction rules](references/interaction_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated Excel workbook when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes user-provided PDF folders and Excel templates locally; OCR accuracy and spreadsheet values require user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
