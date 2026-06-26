## Description: <br>
Complete guide for reading and editing PDF documents with PyMuPDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect, update, and redact PDF documents while preserving the text layer and avoiding image-based PDF workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect visual-only redaction can leave sensitive text extractable from the PDF structure. <br>
Mitigation: Use PyMuPDF redaction annotations with apply_redactions() for sensitive data, then verify by extracting text from the final PDF. <br>
Risk: PDF edits may alter important documents or create misleading replacements. <br>
Mitigation: Work on copies of important PDFs and only modify documents the operator is authorized to edit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/edit-pdf-pdf-editing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown guidance with Python and JavaScript code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; generated edits should be checked against the source PDF and final extracted text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
