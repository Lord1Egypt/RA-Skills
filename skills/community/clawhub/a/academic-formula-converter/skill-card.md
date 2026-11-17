## Description:

Convert LaTeX math formulas in Markdown to styled DOCX or HTML documents with Unicode symbol support for academic writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khimyoung](https://clawhub.ai/user/khimyoung)

### License/Terms of Use:


## Use Case:

Developers, researchers, and academic writers use this skill to convert Markdown documents containing LaTeX-style math into DOCX or styled HTML outputs for easier sharing and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converting untrusted Markdown can carry local image references or raw HTML into generated outputs.

Mitigation: Inspect source Markdown before conversion, avoid untrusted files, and review generated DOCX or HTML before sharing.

Risk: Image handling is under-scoped and may embed files outside the intended image directory.

Mitigation: Use trusted image paths only and prefer a hardened version that restricts images to the selected image directory.

Risk: HTML output may preserve unsafe content from the input document.

Mitigation: Sanitize HTML inputs or outputs and pin reviewed dependencies before deploying in shared workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/khimyoung/skills/academic-formula-converter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with command-line examples and generated DOCX or HTML document outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converts inline and block math formulas and can include referenced images when generating documents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
