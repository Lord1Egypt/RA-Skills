## Description:

交互式图表转PNG/JPG/SVG图片，支持批量导出和多尺寸预设

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content creators use this skill to convert interactive chart, table, SVG, or Canvas content into static image assets for presentations, documents, social sharing, printing, and archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted HTML, SVG, or Canvas JavaScript can include untrusted scripts or active content.

Mitigation: Only use trusted chart markup, or render untrusted inputs in an isolated browser context before exporting images.

Risk: Chart markup may contain secrets, private data, or sensitive labels that become embedded in exported images.

Mitigation: Review and redact source markup and generated images before sharing, publishing, or archiving them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wwbwin/skills/chart-to-image)
- [Publisher Profile](https://clawhub.ai/user/wwbwin)
- [Project Homepage](https://github.com/wwbwin/clawhub-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JSON pattern, and browser-export instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides generation of single-file HTML chart exporters and related PNG, JPG, SVG, batch, presentation, social-size, and print-ready presets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
