## Description: <br>
Comprehensive PDF manipulation toolkit for extracting text and tables, creating PDFs, merging and splitting documents, and handling forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kidaiangel](https://clawhub.ai/user/kidaiangel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to process PDF documents, including extracting content, creating or modifying files, merging or splitting documents, and filling forms with validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs, decrypted documents, extracted text, rendered images, and JSON field files may contain sensitive information. <br>
Mitigation: Use the skill only on PDFs the user is allowed to process, choose output paths deliberately, and treat all derived files according to the source document's sensitivity. <br>
Risk: Filled or generated PDFs may contain incorrect values, misplaced annotations, or invalid form selections. <br>
Mitigation: Review generated and filled PDFs before signing, submitting, or sharing them, and use the provided validation steps for field IDs, values, and bounding boxes. <br>


## Reference(s): <br>
- [PDF Processing Guide](artifact/SKILL.md) <br>
- [PDF Forms Guide](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>
- [Adobe PDF 32000-1:2008 checkbox state reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448) <br>
- [Exploring Fillable Forms with pdfrw](https://westhealth.github.io/exploring-fillable-forms-with-pdfrw.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, and JSON file templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local PDF, image, text, JSON, and spreadsheet files at user-chosen paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
