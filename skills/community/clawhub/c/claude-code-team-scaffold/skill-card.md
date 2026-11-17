## Description:

Initialize a multi-agent AI development framework for a project on Claude Code, including .claude lifecycle hooks, subagent definitions, slash commands, planning files, spec-flow directories, and project/global memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrh07819](https://clawhub.ai/user/lrh07819)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill when starting a Claude Code project that needs a structured AI-assisted development workflow with lifecycle hooks, specialized subagents, slash-command task execution, planning files, and persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Claude Code hooks and memory can affect future agent behavior beyond the initial scaffolded task.

Mitigation: Review generated .claude/settings.json, hook scripts, ~/.claude/CLAUDE.md, and ~/.claude/memory changes before enabling them.

Risk: Quality hooks can invoke npx-based tools whose resolved dependencies may vary if they are not locally pinned.

Mitigation: Use project-pinned dependencies for lint, type-check, and test commands before relying on the hooks.

Risk: Transcript recovery and cross-session memory may surface prior conversation excerpts.

Mitigation: Treat recovered transcripts and memory files as privacy-sensitive and avoid installing this behavior where prior session content should not be reused.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrh07819/skills/claude-code-team-scaffold)
- [Claude Code hooks documentation](https://docs.claude.com/en/docs/claude-code/hooks)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated project files, JSON hook configuration, JavaScript hook scripts, agent definition markdown, slash command markdown, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project scaffolding and may write both repository-local .claude files and global ~/.claude memory or CLAUDE.md content when used as designed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
