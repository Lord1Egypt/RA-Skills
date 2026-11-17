## Description:

Figma设计工具v2 helps agents browse Figma teams, projects, files, design structure, pages, and nodes; export images; manage comments; inspect versions, components, styles, and design variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and automation users use this skill to inspect Figma files, export assets, manage comments, and retrieve component, style, and token information through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command authority that could be used outside its stated Figma purpose.

Mitigation: Use it only for explicit Figma tasks and require confirmation before running commands, writing files, exporting assets, or changing/commenting on Figma content.

Risk: Figma account or token permissions may expose design files or allow unintended changes.

Mitigation: Verify the connected Figma account and token permissions before use, and apply least-privilege access where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/figma-design-paid)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-style responses with possible shell commands, configuration snippets, and exported file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Figma API operations that read or modify Figma content; exported image links may be temporary.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
