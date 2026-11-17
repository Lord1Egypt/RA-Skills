## Description:

Generate professional PDF documents from structured JSON data, including styled titles, tables, lists, highlights, images, and page breaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flexrox](https://clawhub.ai/user/flexrox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn structured JSON content into styled PDF reports or exported documents. It is suited for workflows that need repeatable PDF generation with text, tables, lists, highlights, local images, and page breaks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script writes a PDF to the output path supplied by the user or JSON input.

Mitigation: Review the selected output path before running generation, especially in shared or automated workspaces.

Risk: JSON input may reference local image paths that are embedded into the generated PDF.

Mitigation: Use only intended local images and review generated PDFs before sharing them.

Risk: Generated PDF metadata labels may include German terms.

Mitigation: Review generated PDFs for language labels when non-German metadata text is required.

## Reference(s):

- [PDF Generator Schema Reference](references/schema.md)
- [ClawHub skill page](https://clawhub.ai/flexrox/skills/flow-pdf-generator)
- [Publisher profile](https://clawhub.ai/user/flexrox)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code, Guidance]

**Output Format:** [PDF file generated from JSON input, with Markdown and bash guidance for agent use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to the requested output path or data.output, defaulting to output.pdf; supports styled sections, tables, lists, highlights, local images, and page breaks.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
