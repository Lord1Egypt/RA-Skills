## Description:

Converts Word .docx documents to Markdown and extracts embedded images into a local output directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ooliuhao](https://clawhub.ai/user/ooliuhao)

### License/Terms of Use:


## Use Case:

Developers and technical writers use this skill to convert Word documents into Markdown while preserving headings, lists, tables, and embedded images as local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter writes Markdown and extracted image files to disk.

Mitigation: Use a new or empty output directory and review generated files before relying on them.

Risk: Untrusted or very large DOCX files can create ordinary local file-handling risk during conversion.

Mitigation: Process trusted files in a controlled workspace and avoid running the converter on untrusted or unexpectedly large documents.

Risk: The user-facing documentation and runtime messages are in Chinese.

Mitigation: Have a reviewer who can read the messages confirm usage and error output before deployment in another language environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ooliuhao/skills/docx-to-md)
- [Publisher profile](https://clawhub.ai/user/ooliuhao)

## Skill Output:

**Output Type(s):** [Markdown, Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown files, extracted image files, and Python or CLI invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output to a specified directory or a default document-named output folder; requires Python 3.7+ and python-docx.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
