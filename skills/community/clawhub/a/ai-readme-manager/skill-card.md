## Description:

Manages AI_README.md files so AI agents remember your project conventions across every session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[draco-cheng](https://clawhub.ai/user/draco-cheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to retrieve, initialize, update, validate, and compress AI_README.md files that capture persistent project conventions for code-related work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an MCP server broad influence over code tasks and persistent project guidance.

Mitigation: Install only if the ai-readme-mcp package is trusted, limit use to intended repositories, and review AI_README.md changes like code changes.

Risk: Initialization and update actions can create or modify persistent AI_README.md guidance without clear approval controls.

Mitigation: Require confirmation before init_ai_readme or update_ai_readme and review the resulting guidance before relying on it.

## Reference(s):

- [AI README Manager on ClawHub](https://clawhub.ai/draco-cheng/skills/ai-readme-manager)
- [ai-readme-mcp project homepage](https://github.com/Draco-Cheng/ai-readme-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text guidance, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retrieve, initialize, update, validate, or compress AI_README.md guidance through the configured MCP server.]

## Skill Version(s):

1.7.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
