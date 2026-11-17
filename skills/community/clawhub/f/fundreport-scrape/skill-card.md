## Description:

Fundreport Scrape extracts fund monthly report data from PDFs using text and OCR processing, compares two months, and fills an Excel template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imkiiki](https://clawhub.ai/user/imkiiki)

### License/Terms of Use:

MIT-0

## Use Case:

Financial operations analysts and developers use this skill to extract fund metrics and distribution data from user-provided monthly report PDFs, compare two reporting months, and generate a populated Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer asks for root access to install OCR system dependencies.

Mitigation: Review the installer before use, prefer trusted system package manager installation for Tesseract and Poppler, and install Python packages in a non-root virtual environment with pinned versions.

Risk: Folder-based processing can include more PDF or Excel files than intended.

Mitigation: Use narrow, intentional input folders and explicit output paths before running batch extraction.

Risk: Generated Excel workbooks may contain sensitive financial data.

Mitigation: Treat generated workbooks as sensitive financial documents and store or share them according to the user's data handling requirements.

Risk: OCR and PDF extraction can produce incorrect financial values.

Mitigation: Review extracted values against the source PDFs before relying on the generated workbook.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imkiiki/skills/fundreport-scrape)
- [Batch processing rules](references/batch_processing.md)
- [Extraction templates](references/extraction_templates.json)
- [Field mapping rules](references/field_mapping.md)
- [Interaction rules](references/interaction_rules.md)
- [OCR rules](references/ocr_rules.md)
- [Template learning rules](references/template_learning.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Excel workbook with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a populated .xlsx workbook at a user-specified output path from local PDF and Excel inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
