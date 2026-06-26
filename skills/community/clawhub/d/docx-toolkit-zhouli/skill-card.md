## Description: <br>
Extract text, tables, and images from .docx and legacy .doc files, with support for large documents, CJK text, complex table structures, image deduplication, and image filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to extract document text, tables, and embedded images from Word files for analysis, migration, auditing, and automation pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive content from Word documents may be written to extracted text, image, or manifest outputs. <br>
Mitigation: Treat extracted outputs as sensitive when the source document is sensitive, and store them only in appropriate output directories. <br>
Risk: Image resizing can overwrite files when no separate output directory is provided. <br>
Mitigation: Use an explicit output directory unless in-place resizing is intended. <br>
Risk: Dependency and file-processing behavior runs locally against user-supplied documents. <br>
Mitigation: Install dependencies in a virtual environment and review documents and outputs before using them in downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/docx-toolkit-zhouli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/onlyloveher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated text, image, or JSON manifest files from the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected script: extracted text, tab-delimited tables, extracted image files, optional image context manifests, or resized image files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
