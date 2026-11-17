## Description:

ZeeLin Auto-PPT helps agents create designed presentation PDFs in Google NotebookLM from user-provided content, with optional YouTube sources and PDF/PPTX post-processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a topic or prepared content into a NotebookLM-generated presentation PDF, optionally adding YouTube sources for context. It can also merge generated PDFs, remove likely duplicate pages, and export a cleaned PPTX when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags broad Desktop PDF cleanup behavior and file handling that needs review before installation.

Mitigation: Review the skill before installing, prefer explicit PDF filenames for merge and post-processing operations, and avoid running all-Desktop processing unless every Desktop PDF has been checked.

Risk: NotebookLM and optional YouTube source collection may expose user-provided content to external services.

Mitigation: Use the skill only with non-confidential NotebookLM content and avoid YouTube source collection for sensitive topics.

Risk: Output filenames are passed into Desktop file operations.

Mitigation: Choose simple output filenames without path characters.

## Reference(s):

- [Google NotebookLM](https://notebooklm.google.com/)
- [Deep-research multipart workflow](references/deep-research-multipart-workflow.md)
- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/auto-ppt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated PDF or PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written to the user's Desktop by the bundled scripts.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
