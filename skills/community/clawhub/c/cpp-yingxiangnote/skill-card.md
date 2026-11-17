## Description:

Organizes C++ course PDFs or prepared Markdown into structured Yinxiang Note super notes with headings, code blocks, and tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lonelypatientsk](https://clawhub.ai/user/lonelypatientsk)

### License/Terms of Use:

MIT

## Use Case:

Students, educators, and developers use this skill to turn course PDFs or prepared Markdown into organized notes in a chosen Yinxiang Note notebook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Yinxiang developer token can read and write account content.

Mitigation: Provide the token only when needed, keep it out of files, and revoke it after use.

Risk: Uploading can create a notebook or overwrite an existing note.

Mitigation: Confirm the destination notebook and note GUID before creating or updating content.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lonelypatientsk/skills/cpp-yingxiangnote)
- [Yinxiang Note native-format guide](references/native-format.md)

## Skill Output:

**Output Type(s):** [Markdown, ENML notes, Guidance]

**Output Format:** [Structured Markdown and Yinxiang Note-compatible ENML, with optional notes written to a selected notebook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports headings, code blocks, and tables; scanned pages require visual recognition.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
