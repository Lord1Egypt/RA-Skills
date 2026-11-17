## Description:

Read and generate Word documents with correct structure, styles, and cross-platform compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dnaxxx-hub](https://clawhub.ai/user/dnaxxx-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and document automation agents use this skill to read and generate DOCX files while preserving document structure, styles, sections, numbering, fields, comments, and cross-editor compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Macro-enabled DOCM files can contain active content and present security risk.

Mitigation: Handle DOCM separately from DOCX, inspect macro content, and avoid opening or processing untrusted macro-enabled files without controls.

Risk: Visible document text may omit deleted text, comments, field codes, cached field results, or revision metadata.

Mitigation: When extracting or generating documents, inspect revision, comment, and field XML instead of relying only on visible text.

Risk: Complex formatting can shift across Microsoft Word, LibreOffice, and Google Docs.

Mitigation: Round-trip test important documents in target editors and prefer styles and section properties over manual layout.

## Reference(s):

- [DOCX Editor on ClawHub](https://clawhub.ai/dnaxxx-hub/skills/docx-editor)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown reference guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; the artifact does not run code or request unusual access.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
