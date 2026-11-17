## Description:

Integrates OpenClaw with Claude Code CLI so an agent can read codebases, edit files, run commands, review code, debug issues, and automate development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-11even](https://clawhub.ai/user/mr-11even)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate codebase exploration, file edits, code review, debugging, test writing, commits, and automation tasks from OpenClaw to Claude Code CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing Claude Code with a remote shell installer, which can execute unverified code if followed blindly.

Mitigation: Use official, verifiable Claude Code installation instructions and inspect installation steps before running them.

Risk: Claude Code, MCP servers, hooks, and sub-agents may read code, run commands, change files, and persist configuration or sessions.

Mitigation: Run the skill only in trusted repositories, keep tokens least-privileged, review permission modes and MCP configuration, and inspect proposed file or command changes before accepting them.

## Reference(s):

- [Claude Code hooks documentation](https://code.claude.com/docs/en/hooks.md)
- [ClawHub skill page](https://clawhub.ai/mr-11even/skills/claude-code-openclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may propose or run Claude Code CLI workflows that read, edit, review, and automate repository changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
