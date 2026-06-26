## Description: <br>
Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kidaiangel](https://clawhub.ai/user/kidaiangel) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and document workflow users use this skill to create, read, modify, redline, comment on, and analyze professional Word .docx documents while preserving formatting and review metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to install optional system, npm, or Python dependencies for document conversion and editing. <br>
Mitigation: Use preinstalled or isolated tooling where possible, and review any sudo, global npm install, or pip install command before execution. <br>
Risk: Direct .docx editing can alter professional documents, including tracked changes, comments, formatting, and embedded content. <br>
Mitigation: Work on copies, use the documented redlining workflow for third-party or formal documents, and verify final output with conversion or validation before use. <br>


## Reference(s): <br>
- [Docx Skill on ClawHub](https://clawhub.ai/kidaiangel/document-docx) <br>
- [DOCX library tutorial](docx-js.md) <br>
- [Office Open XML technical reference](ooxml.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python or JavaScript code, and generated or edited DOCX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on local document-processing tools such as pandoc, docx, LibreOffice, Poppler, and defusedxml when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
