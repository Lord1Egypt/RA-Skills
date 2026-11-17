## Description:

Render Mermaid diagrams as beautiful SVG, PNG, or ASCII art with support for flowchart, sequence, state, class, ER, and XY chart types, built-in themes, style presets, CSS customization, interactive preview, and batch rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chouraycn](https://clawhub.ai/user/chouraycn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to render Mermaid diagrams into polished SVG, PNG, ASCII, or rich HTML outputs for documentation, presentations, terminal workflows, and web previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports active local HTML preview behavior and confirmed unsanitized HTML/SVG insertion paths, making untrusted Mermaid input risky.

Mitigation: Use the skill only with trusted .mmd files, skip automatic previews when not needed, and avoid opening generated HTML from untrusted Mermaid input until the @icon and preview innerHTML paths are sanitized.

Risk: Generated diagrams or rich HTML may include content derived from user-provided diagram metadata.

Mitigation: Review generated SVG, PNG, ASCII, or HTML outputs before publishing or embedding them in downstream documents or sites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chouraycn/skills/beautiful-mermaid)
- [Publisher profile](https://clawhub.ai/user/chouraycn)
- [Beautiful Mermaid repository](https://github.com/chouraycn/beautiful-mermaid)
- [Upstream Beautiful Mermaid project](https://github.com/lukilabs/beautiful-mermaid)
- [Mermaid documentation](https://mermaid.js.org/)
- [API configuration](references/api-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated SVG, PNG, ASCII, or HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open an interactive local HTML preview and may batch-render multiple .mmd files.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
