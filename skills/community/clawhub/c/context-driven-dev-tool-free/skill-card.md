## Description:

将项目上下文作为可管理制品，通过结构化文档确保 AI 辅助开发的一致性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent builders, and engineering teams use this skill to create and maintain structured project context documents for new projects, existing codebases, and AI-assisted development alignment. It is intended for work with clear technical requirements or an identifiable technology stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and describes broad file, API, and automation abilities beyond its context-document purpose.

Mitigation: Use it primarily to read project context and create context Markdown files; explicitly approve any shell command, package installation, external API call, or broad repository modification before execution.

Risk: Generated project context can become an authoritative input for later AI-assisted development even when it contains incorrect assumptions.

Mitigation: Review generated context documents before relying on them for implementation, debugging, deployment, or cross-session alignment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/context-driven-dev-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured steps, code blocks, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese interaction and may produce project context files, validation snippets, or command suggestions for agent review.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
