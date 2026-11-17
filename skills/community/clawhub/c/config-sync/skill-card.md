## Description:

Syncs AI coding assistant configuration files from `.claude/rules/` or `CLAUDE.md` into native formats for Codex, Gemini CLI, Cursor, GitHub Copilot, Windsurf, Cline/Roo, Aider, Kiro, Amazon Q, Goose, Trae AI, Zed, Amp, OpenCode, and Warp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nadalpiantini](https://clawhub.ai/user/nadalpiantini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep AI assistant instruction files synchronized from one canonical Claude rules source across repositories that support multiple coding assistants. It can preview changes, initialize rules from an existing `CLAUDE.md`, and generate only selected tool configurations when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill can rewrite AI assistant instruction files in the target repository.

Mitigation: Run it first with `--dry-run` and review generated files before committing or using them with AI coding assistants.

Risk: Symlinked projects may allow reads or writes outside the intended repository.

Mitigation: Use the skill only on trusted repositories and inspect the target tree for symlinks before running it.

Risk: Rules copied across assistants can become persistent, always-on guidance in multiple tools.

Mitigation: Review generated instructions for scope, sensitivity, and assistant-specific behavior before adoption.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nadalpiantini/skills/config-sync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown and plain-text configuration files written to repository paths, with shell command guidance for invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews, selected tool targets, and initialization from an existing CLAUDE.md.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
