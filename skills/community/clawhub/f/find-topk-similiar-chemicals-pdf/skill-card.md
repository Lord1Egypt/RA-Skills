## Description: <br>
PDF manipulation toolkit. Extract text/tables, create PDFs, merge/split, fill forms, for programmatic document processing and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and document-processing agents use this skill to extract PDF content, create or modify PDF files, merge and split documents, and fill PDF forms with local utilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags unrelated schematic-generation and hosted-platform guidance that users may not expect in a PDF utility skill. <br>
Mitigation: Review those instructions before deployment and ignore or remove them if the intended use is limited to PDF processing. <br>
Risk: PDF processing can expose sensitive document contents through generated JSON, images, extracted text, or output PDFs. <br>
Mitigation: Use the utilities only on documents the operator is authorized to process, store intermediate and output files in protected locations, and delete sensitive intermediates when finished. <br>
Risk: PDF passwords or form values may be exposed if placed directly in shell history or source files. <br>
Mitigation: Avoid hard-coding secrets in commands or code and pass sensitive values through safer local secret-handling workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wu-uk/find-topk-similiar-chemicals-pdf) <br>
- [Publisher profile](https://clawhub.ai/user/wu-uk) <br>
- [forms.md](forms.md) <br>
- [reference.md](reference.md) <br>
- [PDF 32000-1:2008 reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, JavaScript, shell commands, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local PDF, image, text, JSON, and spreadsheet files when the recommended utilities are executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
