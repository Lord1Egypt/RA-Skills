## Description:

Delegate coding tasks to Claude Code CLI via background process. Use when: building features, reviewing PRs, refactoring codebases, or iterative coding that needs file exploration. Supports interactive PTY mode for confirmations/permissions and headless pipe mode for automation. NOT for: simple one-liner fixes (just edit), reading code (use read tool), or any work in ~/.openclaw/ workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atelypham](https://clawhub.ai/user/atelypham)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to delegate substantial coding work, PR review, refactoring, and long-running implementation tasks to Claude Code CLI from OpenClaw while managing PTY, headless, session, and permission-mode workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches Claude Code with project-level coding authority and includes high-impact background execution patterns.

Mitigation: Use restricted tools and explicit work directories, monitor or stop background sessions, and reserve broad edit permissions for intentional coding tasks.

Risk: Shell-command examples can become unsafe if untrusted text is copied directly into command strings.

Mitigation: Avoid interpolating untrusted text into shell commands and review command arguments before execution.

Risk: Unpinned installation of Claude Code can change behavior across releases.

Mitigation: Consider pinning the Claude Code package version and reviewing release changes before updating.

Risk: Long-running handoff and cleanup workflows can resume stale state or target the wrong temporary path.

Mitigation: Review HANDOFF.md before resuming and verify temporary paths before cleanup.

## Reference(s):

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/atelypham/skills/claude-code-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PTY, background-session, permission-mode, budget-cap, and tool-restriction guidance for Claude Code CLI execution.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata; artifact frontmatter states 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
