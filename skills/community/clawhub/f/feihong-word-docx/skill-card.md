## Description:

Create, inspect, and edit Microsoft Word documents and DOCX files with reliable styles, numbering, tracked changes, tables, sections, and compatibility checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunyue1977](https://clawhub.ai/user/sunyue1977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and document automation agents use this skill when a task involves creating, inspecting, or editing Word/DOCX files where styles, numbering, tracked changes, comments, fields, tables, sections, or round-trip compatibility matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DOCX review workflows can expose hidden comments, revisions, deleted text, and field data inside a document.

Mitigation: Use the skill only with documents the user is comfortable having the agent inspect or edit, and review hidden review metadata before sharing outputs.

Risk: Complex Word documents can drift across Word, LibreOffice, Google Docs, and conversion tools, especially around tables, headers, fields, and sections.

Mitigation: Perform round-trip compatibility checks in the target editor and inspect document structure when layout, fields, or tracked changes matter.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunyue1977/skills/feihong-word-docx)
- [Skill Homepage](https://clawic.com/skills/word-docx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents toward structure-preserving DOCX workflows and compatibility checks.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and _meta.json report 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
