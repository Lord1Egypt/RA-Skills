## Description:

Creates, reads, edits, validates, and manipulates Microsoft Word .docx documents, including formatting, tracked changes, comments, images, and content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, document authors, and document-processing agents use this skill to create polished Word documents and to inspect or modify existing .docx files. It supports workflows such as extracting content, applying formatting, managing tracked changes and comments, converting legacy Word files, and validating Office XML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risky local execution patterns may allow shared temporary files or LibreOffice macro handling to hijack LibreOffice runs.

Mitigation: Review or fix the temporary-file and LibreOffice macro handling before installation, run the skill in an isolated environment, and avoid shared /tmp execution.

Risk: Sensitive or untrusted documents and comment text can increase exposure when processed by local document tooling.

Mitigation: Use extra caution with sensitive or untrusted documents and comment text, and review outputs before relying on them.

Risk: Global npm installs can make dependency behavior harder to control.

Mitigation: Pin npm dependencies locally instead of relying on global installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/docx-processor-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with code and shell command examples; generated or edited .docx files when used for document creation or modification.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows require local tooling such as docx-js, pandoc, LibreOffice, and bundled validation scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
