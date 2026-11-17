## Description:

Auto-selects and applies design systems from awesome-design-md based on project type and task context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[html1602](https://clawhub.ai/user/html1602)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose UI design systems, generate local design references, and guide implementation choices for pages, components, dashboards, documentation, marketing sites, and related frontend work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-activate broadly for design, styling, UI, UX, layout, and component work.

Mitigation: Install it only in workspaces where broad design assistance is intended, or invoke it explicitly when an agent platform supports scoped activation.

Risk: The skill may fetch mutable remote Markdown design references.

Mitigation: Prefer pinned or reviewed design sources before applying downloaded guidance to production work.

Risk: The skill can lead an agent to write local design reference files or run optional conversion commands that create agent skill files.

Mitigation: Review generated file changes before keeping them, and run conversion commands only when intentionally installing the skill into another agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/html1602/skills/auto-design-clawhub)
- [Skill homepage](https://github.com/moyubox/auto-design)
- [awesome-design-md design system collection](https://github.com/VoltAgent/awesome-design-md)
- [awesome-design-md raw design reference template](https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/{brand}/DESIGN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local design reference files such as DESIGN.md, Docs/Design/{brand}-DESIGN.md, and Docs/DevLog/YYYY-MM-DD_design.md when followed by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
