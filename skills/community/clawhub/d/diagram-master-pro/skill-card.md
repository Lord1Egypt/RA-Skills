## Description:

图表制作大师(专业版) helps agents create, batch-generate, theme, export, version, and manage SVG-based technical diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, documentation engineers, and technical authors use this skill to produce reusable technical diagrams, batch-generate diagram assets, apply custom themes, export SVG/PNG/PDF outputs, and manage diagram versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for read, write, and command-execution authority for diagram generation and export workflows.

Mitigation: Run it in a constrained workspace, review proposed shell commands before execution, and limit file access to the documents and output directories needed for the task.

Risk: The security evidence says network/API behavior is under-disclosed, and the input schema includes an optional callback URL.

Mitigation: Disable or review callback URLs and external API use before processing private documents or internal architecture material.

Risk: Interactive SVG output can contain active behavior when viewed in compatible environments.

Mitigation: Open interactive SVGs only from trusted runs, review links and embedded behavior, and prefer static exports for broad sharing.

## Reference(s):

- [Detailed Reference](references/detail.md)
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/diagram-master-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SVG/code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify local diagram files and exported image/document assets when run by an agent with write and command-execution tools.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
