## Description:

精英前端设计-专业版 helps agents design and generate enterprise frontend systems, including multi-page applications, React/Vue component libraries, design tokens, brand consistency, responsive behavior, and motion guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend teams use this skill to have an agent create or modify frontend project assets for SaaS and enterprise web applications. It is most relevant when the work needs consistent design tokens, React or Vue components, responsive layouts, accessibility considerations, and coordinated page or component motion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to generate or modify frontend project files.

Mitigation: Review generated files before merging or deploying changes, especially in repositories that contain private code or secrets.

Risk: The skill may propose shell commands, npm installs, callback URLs, or API destinations as part of frontend workflows.

Mitigation: Approve only commands and destinations that are expected for the project, and reject unexpected package installs or external callbacks.

## Reference(s):

- [Detailed frontend design reference](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/elite-frontend-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, configuration snippets, shell commands, and generated frontend source files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include HTML/CSS, React, Vue, TypeScript, design token JSON or CSS variables, and implementation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
