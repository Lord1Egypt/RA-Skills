## Description:

SOP for writing, loading, and evolving a project-level convention file (CONVENTIONS.md / CLAUDE.md / .cursor/rules / .clinerules / AGENTS.md) so that a coder-agent reliably respects your codebase's style choices every session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to decide when to create a project conventions file, draft concise rules, wire the file into common coder-agent tools, and verify that the agent actually loaded it. It is intended for projects that will be revisited across multiple coding-agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Convention files can influence future coding-agent sessions and may encode stale, overly broad, or sensitive project guidance.

Mitigation: Keep rules short, repo-scoped, and secret-free; review user-global or always-loaded rules before using them.

Risk: A conventions file is guidance rather than enforcement, so agents may ignore vague, conflicting, or oversized rule sets.

Mitigation: Use concrete verifiable rules, verify loading with the tool's introspection path, and move must-hold requirements into lint, hooks, or CI.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/agentsope/skills/agentsop-conventions-pinning)
- [R1 source evidence](references/R1-source-evidence.md)
- [R2 tool equivalents](references/R2-tool-equivalents.md)
- [Aider CONVENTIONS.md documentation](https://aider.chat/docs/usage/conventions.html)
- [Claude Code memory documentation](https://code.claude.com/docs/en/memory)
- [Cursor rules documentation](https://cursor.com/docs/rules)
- [Cline rules documentation](https://docs.cline.bot/customization/cline-rules)
- [CrewAI agents documentation](https://docs.crewai.com/en/concepts/agents)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with file templates, configuration snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or revise repo-scoped convention files such as CONVENTIONS.md, CLAUDE.md, .cursor/rules/*.mdc, .clinerules/*.md, or AGENTS.md.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
