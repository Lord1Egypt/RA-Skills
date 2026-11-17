## Description:

Extracts text from Word, PDF, and Excel files using python-docx, pdfplumber, pandas, and openpyxl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect DOCX, PDF, XLS, and XLSX files and return extracted document text for downstream analysis or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill description and examples advertise write or edit behavior that is not implemented in the provided artifact.

Mitigation: Use the skill for document text extraction only, and verify any document modification workflow separately before relying on it.

Risk: Extracted document text may include sensitive information from user-provided files.

Mitigation: Review file handling and downstream prompts so extracted content is shared only with approved tools, models, and storage locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/skills/doc-handler)
- [Publisher profile](https://clawhub.ai/user/xaiohuangningde)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document text extraction only; editing or writing output is not implemented in the provided artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
