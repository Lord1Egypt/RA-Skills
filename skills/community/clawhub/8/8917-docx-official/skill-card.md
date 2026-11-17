## Description:

Converts prepared Markdown or text into Chinese official-document DOCX files and can optionally produce PDF output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blicae8917](https://clawhub.ai/user/blicae8917)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-preparation agents use this skill to turn already prepared Markdown or text into formatted Chinese official-document Word files, including reports, notices, meeting minutes, plans, and similar formal documents. Users may request PDF output when LibreOffice is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional PDF path compiles and loads a native LibreOffice hook with LD_PRELOAD.

Mitigation: Prefer the DOCX-only path for sensitive documents, or require the publisher to remove or clearly document the native helper before production use.

Risk: PDF conversion relies on LibreOffice child-process execution and temporary native artifacts.

Mitigation: Run PDF conversion only in a controlled environment and require safer temporary-file handling plus a minimized child-process environment before handling sensitive documents.

## Reference(s):

- [Official format rules](artifact/references/official-format-rules.md)
- [ClawHub skill page](https://clawhub.ai/blicae8917/skills/8917-docx-official)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples and generated DOCX or PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 for DOCX output; optional PDF output requires gcc and LibreOffice/soffice.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
