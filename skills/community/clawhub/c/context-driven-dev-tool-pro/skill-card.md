## Description:

上下文驱动开发（专业版） helps developers and teams create, analyze, and maintain project context documents so AI-assisted development stays consistent across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to initialize or adapt project context files, capture product and technical decisions, and align AI-assisted development across sessions and workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file and shell authority while managing project context documents.

Mitigation: Use explicit, narrow prompts; ask for a dry run or file list before writes or commands; review changes before applying them.

Risk: Security evidence notes inconsistent guidance about API keys and external or API use.

Mitigation: Do not provide API keys, callback URLs, or credentials unless independently confirmed as necessary, and prefer scoped environment variables over inline secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/context-driven-dev-tool-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code snippets, shell commands, configuration examples, and generated or updated context files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require read, write, edit, and shell access in the target repository; review proposed file changes and commands before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
