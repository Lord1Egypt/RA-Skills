## Description:

前端设计工具专业版 helps agents create and govern front-end design systems for teams, including design tokens, component libraries, multi-theme sites, consistency checks, accessibility audits, and performance budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and external teams use this skill to have an agent draft and govern front-end design systems, component libraries, multi-theme pages, consistency checks, accessibility audits, and performance-budget guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose modifications to front-end project files or design-system configuration.

Mitigation: Review generated diffs, keep source control enabled, and apply changes in a branch before merging.

Risk: The skill may suggest npm-based audit or build commands.

Mitigation: Review commands before execution, use trusted package sources, and avoid running commands that install unreviewed dependencies.

Risk: Private repository tokens or other credentials could be exposed if included directly in configuration examples.

Mitigation: Store credentials in environment variables or secret managers and keep them out of generated files and logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/frontend-design-other-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CSS, JavaScript, JSON, shell-command, and text examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose front-end file changes, design-system configuration, audit reports, and command-line checks for human review.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
