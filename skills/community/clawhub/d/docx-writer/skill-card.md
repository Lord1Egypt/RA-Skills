## Description:

Creates formatted Word documents with templates, footnotes, tables, images, and editable or image-rendered LaTeX formulas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomuiv](https://clawhub.ai/user/tomuiv)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, researchers, and developers use this skill to generate formatted Word documents, including academic papers, reports, news articles, and scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compiling user-provided LaTeX with local tools lacks a clear sandbox or strict input limits.

Mitigation: Use trusted formulas and documents; isolate execution in a container or restricted workspace for third-party content.

Risk: Chinese-specific formatting defaults may not suit other languages.

Mitigation: Review and adjust the document templates before using them for non-Chinese documents.

## Reference(s):

- [docx-writer on ClawHub](https://clawhub.ai/tomuiv/skills/docx-writer)

## Skill Output:

**Output Type(s):** [Files, Code]

**Output Format:** [DOCX documents; optional PNG formula images and Python or YAML/JSON content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formula output can be editable Word math or rendered images, depending on available tools.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
