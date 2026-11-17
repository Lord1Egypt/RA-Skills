## Description:

Comprehensive document creation, editing, and analysis for .docx files, including tracked changes, comments, formatting preservation, and text extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kidaiangel](https://clawhub.ai/user/kidaiangel)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and document-focused agents use this skill to create, inspect, edit, redline, convert, and validate professional Word documents while preserving formatting and review metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes privileged or global dependency installation guidance.

Mitigation: Treat sudo, apt, npm global, and pip setup commands as administrator-reviewed setup steps rather than commands an agent should run automatically.

Risk: The skill reads and modifies local Office documents and may process untrusted Office archives.

Mitigation: Process untrusted DOCX, PPTX, or XLSX files only in a sandbox with resource limits and review outputs before using modified documents.

Risk: Document editing and redlining workflows can introduce incorrect or unintended changes to professional, legal, academic, business, or government documents.

Mitigation: Require human review of generated edits, tracked changes, and final converted documents before relying on them.

## Reference(s):

- [DOCX Library Tutorial](docx-js.md)
- [Office Open XML Technical Reference](ooxml.md)
- [ClawHub Skill Page](https://clawhub.ai/kidaiangel/skills/document-docx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets; generated or modified Office document files may result from following the guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document operations may rely on local tools such as pandoc, LibreOffice, Poppler, docx-js, and Python helpers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
