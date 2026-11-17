## Description:

Call Claude Code as a non-interactive coding agent on the same machine as OpenClaw for delegated coding, refactoring, bug fixing, code analysis, batch reviews, and automated CI/CD checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxuzzwz](https://clawhub.ai/user/xxuzzwz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to invoke local Claude Code for code writing, refactoring, troubleshooting, analysis, batch review, and CI/CD code-check workflows. It provides command templates, permission modes, output-format guidance, timing expectations, and post-task review checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to run Claude Code locally with file, shell, and credential access.

Mitigation: Use the lowest permission mode that satisfies the task, prefer read-only or tightly scoped modes, and review proposed commands before execution.

Risk: The documented full-access mode can bypass permission prompts in trusted-project workflows.

Mitigation: Avoid `--dangerously-skip-permissions` except in isolated, trusted workspaces with explicit operator approval.

Risk: Credential troubleshooting can encourage broader environment exposure of API keys or auth tokens.

Mitigation: Keep credentials narrowly scoped, avoid moving API keys into broadly inherited shell startup paths, and verify which environment variables are exposed before running local commands.

Risk: Installing or invoking a local Claude Code CLI may execute an unverified toolchain.

Mitigation: Pin or verify the Claude Code CLI before global installation and confirm the expected binary is on PATH.

## Reference(s):

- [Stream-JSON Processing](references/streaming.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/xxuzzwz/skills/claude-code-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, command tables, checklists, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes permission-mode recommendations, stream-json parsing examples, and troubleshooting checks for local Claude Code execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
