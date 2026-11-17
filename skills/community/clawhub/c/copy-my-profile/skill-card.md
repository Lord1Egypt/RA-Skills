## Description:

Extracts a standardized cross-tool user profile from AI agent memory files and produces a portable Markdown profile that can be reviewed and imported into another AI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-tool users use this skill to export their long-term AI assistant memory into a portable Markdown profile for reuse across tools such as Claude Code, Codex CLI, Cursor, Cline, Continue, Aider, ChatGPT, and Claude.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported profiles may include sensitive or overly broad personal, project, or instruction data from AI memory/config files.

Mitigation: Review the generated profile before sharing or importing it, remove secrets and project-specific instructions, and prefer manual diffs for changes.

Risk: Persistent cross-tool imports can carry repository-specific rules into global memory and affect unrelated future sessions.

Mitigation: Import only intentionally scoped entries, avoid global storage for repository-derived rules, and use project-scoped memory where possible.

## Reference(s):

- [Profile Template](artifact/references/profile-template.md)
- [AI Tools Memory File Map](artifact/references/tools-memory-map.md)
- [Import Prompts](artifact/references/import-prompts.md)
- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/copy-my-profile)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown profile file plus inline Markdown response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes ./my-profile.md, preserves five profile categories, and includes review/import notes for the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
