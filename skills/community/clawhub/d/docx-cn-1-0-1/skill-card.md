## Description:

Word document processing skill for creating, reading, editing, validating, converting, and repairing .docx files, including formatting, tables, images, comments, and tracked changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin](https://clawhub.ai/user/binbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users use this skill to create, inspect, convert, edit, validate, and package Word .docx documents. It is especially relevant for workflows involving docx-js generation, raw OOXML edits, comments, tracked changes, and LibreOffice-based conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LibreOffice-based conversion and tracked-change acceptance use local execution, a /tmp LibreOffice profile, and may use LD_PRELOAD native code.

Mitigation: Review before installing, run only in an isolated workspace, use documents you trust, and clean temporary LibreOffice profile or shim artifacts after use.

Risk: The skill can mutate Office documents while accepting changes, packing XML, repairing validation issues, or converting formats.

Mitigation: Work on copies, keep backups of important files, and inspect or validate outputs before replacing source documents.

Risk: The documentation suggests a global npm install for docx-js.

Mitigation: Prefer project-local dependency installation or another controlled package-management approach instead of global installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binbin/skills/docx-cn-1-0-1)
- [OpenClaw fork metadata](https://github.com/anthropics/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with code and shell command examples; generated or modified Office document files when executed by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce document mutations, validation reports, extracted XML, converted PDFs or images, and repaired Office packages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
