## Description:

Bold UI helps agents apply professional design templates, design strategy, polished icons, and framework-specific UI code across web, mobile, and desktop projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wh19981224](https://clawhub.ai/user/wh19981224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-focused coding agents use this skill to analyze an application's product goals, choose or adapt a visual direction, and generate UI styling, icons, design tokens, components, or layout guidance across web, mobile, and desktop projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom template imports from GitHub can add untrusted template instructions that may persist across projects.

Mitigation: Import templates only from trusted repositories and review each imported manifest and description before using it.

Risk: Global template installation can make an unsafe or unsuitable template available beyond the current project.

Mitigation: Prefer project-scoped templates unless the source is trusted and the template has been reviewed for cross-project use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wh19981224/skills/bold-ui)
- [Template Registry](artifact/templates/index.yaml)
- [Tailwind CSS Adapter](artifact/adapters/tailwindcss.md)
- [CSS Variables Adapter](artifact/adapters/css-variables.md)
- [Iconify API Example](https://api.iconify.design/lucide/arrow-right.svg?height=24)

## Skill Output:

**Output Type(s):** [Text, Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and generated UI code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate design tokens, base components, layout code, icon SVGs, and framework-specific styling instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
