## Description: <br>
DOCX Toolkit extracts text, tables, and images from .docx and legacy .doc files, including CJK text and complex table structures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacjiang](https://clawhub.ai/user/zacjiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing teams use this skill to extract Word document text, tables, and embedded images for analysis, migration, auditing, or batch processing pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted text, images, and optional context manifests may contain sensitive document content. <br>
Mitigation: Process only documents the user is allowed to handle, keep output folders private, and enable context manifests only when needed. <br>
Risk: Image resizing can overwrite originals when no separate output directory is provided. <br>
Mitigation: Use a separate output directory when resizing images to preserve source files. <br>
Risk: The scripts rely on local Python dependencies for document and image processing. <br>
Mitigation: Install dependencies only in an environment where the user trusts the packages and execution context. <br>


## Reference(s): <br>
- [DOCX Toolkit on ClawHub](https://clawhub.ai/zacjiang/docx-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text files, extracted image files, JSON image manifests, and Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local document processing; extracted outputs may contain sensitive document text, images, and context snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
