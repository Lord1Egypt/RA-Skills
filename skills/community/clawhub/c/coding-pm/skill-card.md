## Description:

Your AI project manager delegates coding tasks to Claude Code running in the background, reviews plans, gates approval, monitors progress, validates with 3-layer testing, and reports results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacehxw](https://clawhub.ai/user/horacehxw)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to manage coding tasks through a PM/QA workflow that delegates implementation to a background Claude Code agent while preserving plan approval, progress monitoring, validation, and merge control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to disable workspace-only filesystem boundaries and may give a background Claude Code process broad project and home-directory access.

Mitigation: Run it in a dedicated container, VM, or low-privilege account with no unrelated secrets, and re-enable tighter filesystem boundaries when not using the skill.

Risk: Execution uses non-interactive background coding agents with broad authority to edit code, run tests, and commit changes.

Mitigation: Use the plan approval gate, inspect diffs and test results before merge, and avoid production repositories until scoped filesystem access and safer cleanup are added.

Risk: The security guidance identifies missing task-name validation, prompt quoting hardening, scoped filesystem access, and safer cancel cleanup.

Mitigation: Avoid untrusted task names or sensitive repositories, and treat the skill as requiring additional hardening before use in high-risk environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/horacehxw/skills/coding-pm)
- [Supervisor Protocol](references/supervisor-prompt.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports, plans, command invocations, and validation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs work in isolated git worktrees and uses structured progress markers for plan, checkpoint, decision, error, and done states.]

## Skill Version(s):

0.4.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
