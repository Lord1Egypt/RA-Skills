## Description: <br>
Generate professional Word, Excel, and PDF documents with rich formatting, tables, images, and layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnblxj](https://clawhub.ai/user/lnblxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to generate local DOCX, XLSX, and PDF reports, invoices, spreadsheets, and formatted exports from JSON configurations and optional templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation and local file generation can affect the user's environment or write to unintended paths. <br>
Mitigation: Install Python dependencies in a trusted environment and confirm configuration, template, image, and output paths before running the generators. <br>
Risk: Excel values beginning with '=' are interpreted as formulas. <br>
Mitigation: Use formula-prefixed values only when formulas are intended; sanitize or escape untrusted spreadsheet text before generation. <br>


## Reference(s): <br>
- [Word Document Configuration Schema](references/word_schema.md) <br>
- [Excel Spreadsheet Configuration Schema](references/excel_schema.md) <br>
- [PDF Document Configuration Schema](references/pdf_schema.md) <br>
- [ClawHub Release Page](https://clawhub.ai/lnblxj/document-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Configuration, Shell commands, Guidance] <br>
**Output Format:** [JSON configurations and local DOCX, XLSX, or PDF files, with Markdown guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates files at user-specified output paths; supports optional template and image paths.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
