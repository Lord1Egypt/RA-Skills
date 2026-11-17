## Description:

Creates, reads, edits, validates, and analyzes Microsoft Word .docx documents, including formatting, tables, images, tracked changes, comments, and format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

Anthropic Consumer Terms of Service or Commercial Terms of Service

## Use Case:

Developers and document-processing agents use this skill to create, inspect, convert, edit, validate, and repair Microsoft Word documents. It is especially relevant when an agent needs to work directly with DOCX XML, comments, tracked changes, tables, images, or LibreOffice-based conversions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes LibreOffice and local document-processing code, including mechanisms that may compile or preload native components.

Mitigation: Install and run it only in a sandboxed environment where local execution, native code, and document conversion are acceptable.

Risk: Office documents can be unpacked, edited, converted, and repacked, which can alter document contents or expose parser risks when inputs are untrusted.

Mitigation: Process only trusted files where possible, work on copies, and validate generated documents before sharing or relying on them.

Risk: The skill writes to /tmp and may use persistent LibreOffice temporary profiles.

Mitigation: Clear or isolate temporary directories and LibreOffice profiles between runs, especially when handling sensitive documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/docx-cn)
- [OpenClaw fork reference](https://github.com/anthropics/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, shell commands, and generated or modified Office document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, unpack, validate, repair, or modify .docx, .doc, .pdf, image, XML, and temporary LibreOffice profile files through local tools.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
