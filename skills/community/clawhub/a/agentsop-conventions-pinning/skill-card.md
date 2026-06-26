## Description: <br>
SOP for writing, loading, and evolving a project-level convention file such as CONVENTIONS.md, CLAUDE.md, .cursor/rules, .clinerules, or AGENTS.md so a coder-agent can consistently follow project style choices across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide when project-level agent conventions are worthwhile, write concise convention files, wire them into tools such as Aider, Claude Code, Cursor, Cline, and CrewAI, and verify that agents actually load and follow them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated convention files may persistently steer future coding agents in ways that are incorrect, stale, or inconsistent with the current codebase. <br>
Mitigation: Review generated convention files before committing them, keep rules concise and concrete, and periodically remove stale or conflicting rules. <br>
Risk: Shared convention files may accidentally include secrets, private paths, or sensitive internal details. <br>
Mitigation: Do not place secrets or private credentials in committed convention files; use gitignored local files or secret-management tooling for sensitive context. <br>
Risk: Convention files are guidance rather than hard enforcement, so agents may still ignore vague or conflicting rules. <br>
Mitigation: Use hooks, lint, tests, or CI for requirements that must always hold, and verify convention loading with tool-specific introspection or an A/B task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentsope/agentsop-conventions-pinning) <br>
- [Source evidence](references/R1-source-evidence.md) <br>
- [Tool equivalents](references/R2-tool-equivalents.md) <br>
- [Aider conventions documentation](https://aider.chat/docs/usage/conventions.html) <br>
- [Claude Code memory documentation](https://code.claude.com/docs/en/memory) <br>
- [Cursor rules documentation](https://cursor.com/docs/rules) <br>
- [Cline rules documentation](https://docs.cline.bot/customization/cline-rules) <br>
- [CrewAI agents documentation](https://docs.crewai.com/en/concepts/agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with templates, tables, and inline shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update convention files such as CONVENTIONS.md, CLAUDE.md, AGENTS.md, .cursor/rules/*.mdc, or .clinerules/*.md.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
