## Description: <br>
Comprehensive PDF manipulation toolkit for extracting text and tables, creating PDFs, merging and splitting documents, and handling form filling workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and agents use this skill to inspect, manipulate, generate, and fill PDF documents, including court and other structured forms that may or may not expose fillable fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes local PDFs, which may contain sensitive personal, legal, or commercial information. <br>
Mitigation: Run it only on documents you are authorized to process and store generated PDFs, images, text extracts, and JSON field files according to the document's sensitivity. <br>
Risk: PDF password removal and decrypted output can expose protected document contents. <br>
Mitigation: Use password-removal steps only for PDFs you are authorized to unlock and protect decrypted copies with the same care as the original document. <br>
Risk: Incorrect bounding boxes or field values can fill a form inaccurately. <br>
Mitigation: Follow the artifact workflow to generate validation images, run bounding-box checks, inspect the rendered result, and keep backups before overwriting originals. <br>


## Reference(s): <br>
- [PDF Form Filling Workflow](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>
- [Adobe PDF 32000-2008 Standard](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448) <br>
- [ClawHub Skill Release](https://clawhub.ai/wu-uk/court-form-filling-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text, markdown] <br>
**Output Format:** [Markdown instructions with inline Python and shell command examples, plus generated JSON inputs for PDF form scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local PDF, PNG, JSON, text, spreadsheet, and image files through user-run tools.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
