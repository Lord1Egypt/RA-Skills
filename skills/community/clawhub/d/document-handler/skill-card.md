## Description: <br>
Read, extract text and metadata, and convert documents in formats like PDF, DOCX, XLSX, PPTX, EPUB, RTF, and OpenDocument. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect user-provided document files, extract text and metadata, and convert PDFs into images for OCR or visual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document text and metadata may contain sensitive information and can enter the agent context during extraction. <br>
Mitigation: Use the skill only on documents intentionally provided for processing, and avoid sensitive files unless sharing extracted content and metadata with the agent is acceptable. <br>
Risk: Document conversion can create or overwrite output files in the selected output directory. <br>
Mitigation: Choose output paths deliberately and review generated files before relying on or sharing them. <br>
Risk: Some documents may extract incompletely, including scanned PDFs, encrypted PDFs, complex formatting, or RTF metadata. <br>
Mitigation: Review extraction results for completeness and use OCR, passwords, or specialized table extraction tools when the document format requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Neckr0ik/document-handler) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text, metadata text, Markdown guidance, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local user-provided document files; PDF image conversion writes PNG files to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
