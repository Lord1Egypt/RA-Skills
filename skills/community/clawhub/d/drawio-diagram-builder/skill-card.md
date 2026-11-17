## Description:

Create, edit, replicate, and iteratively refine editable research and technical diagrams in diagrams.net/draw.io (.drawio XML) from prompts, papers, repositories, screenshots, or existing diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holdyounger](https://clawhub.ai/user/holdyounger)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and technical writers use this skill to author editable draw.io diagrams, reproduce reference figures, and refine architecture or research visuals through XML validation and screenshot-based review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted diagrams.net preview can send diagram XML to diagrams.net.

Mitigation: Use the hosted preview only for non-sensitive diagrams; use a local or offline draw.io workflow for confidential architecture, research, or business diagrams.

Risk: Unpinned npx package installation may execute code from the configured npm source.

Mitigation: Avoid unpinned npx installs unless the npm source is trusted.

Risk: Preview serving can expose local files if bound too broadly.

Mitigation: Keep preview serving bound to 127.0.0.1.

## Reference(s):

- [Draw.io Diagram Workflow](references/drawio-workflow.md)
- [Diagram Intake And Self-Supervision Protocol](references/self-supervision-and-intake.md)
- [Draw.io XML Authoring Notes](references/xml-authoring.md)
- [XML Pre-Flight Quality Checks](references/xml-preflight.md)
- [Style Extraction Protocol](references/style-extraction.md)
- [Top-Conference Computer-Science Figure Style](references/topconf-paper-style.md)
- [Editable Primitive Icon Recipes](references/primitive-icons.md)
- [Reference Image Replication Protocol](references/reference-replication-protocol.md)
- [Bundled Icon Assets](assets/icons/ICON-MANIFEST.md)
- [Bundled Reference Images](assets/reference-images/REFERENCE-IMAGES.md)
- [diagrams.net Embed](https://embed.diagrams.net/)
- [Tabler Icons](https://github.com/tabler/tabler-icons)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with XML, draw.io file content, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces editable .drawio XML as the primary artifact and may generate local preview HTML or validation logs as supporting artifacts.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
