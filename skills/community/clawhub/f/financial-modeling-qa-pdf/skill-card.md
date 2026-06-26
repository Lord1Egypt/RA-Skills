## Description: <br>
PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging or splitting documents, and filling or analyzing forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, analysts, and agent users can use this skill to process PDF documents, extract content, generate or modify PDFs, and complete PDF forms with local helper scripts and library guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes PDFs and creates local output files, which can expose or alter documents outside the intended workflow if used on the wrong inputs. <br>
Mitigation: Use only PDFs you are authorized to access and keep generated files in deliberate, controlled output paths. <br>
Risk: Filled, decrypted, merged, or generated PDFs may be inaccurate or overwrite important files if field mappings, annotations, or paths are wrong. <br>
Mitigation: Review generated PDFs before relying on them and choose output filenames that do not replace important documents. <br>


## Reference(s): <br>
- [PDF form workflow](references/forms.md) <br>
- [PDF Processing Advanced Reference](references/reference.md) <br>
- [PDF 32000-1:2008 field states](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448) <br>
- [Exploring fillable forms with pdfrw](https://westhealth.github.io/exploring-fillable-forms-with-pdfrw.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, and shell command examples; helper scripts can create JSON, images, and PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local text, image, JSON, and PDF artifacts for PDF processing workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
