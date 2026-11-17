## Description:

A text editor for LLMs, not humans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frane](https://clawhub.ai/user/frane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide coding agents through stateful, command-line file editing with versioned history, conflict detection, annotations, transactions, and optional MCP access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages use of an external editor with persistent workspace state and cross-session annotations.

Mitigation: Treat annotations as untrusted context and verify them against the current user request and repository state before acting.

Risk: Installation paths can write agent skills, MCP entries, or configuration files.

Mitigation: Review commands that modify agent configuration or skill directories before execution.

Risk: The curl-based installer executes a remote shell script.

Mitigation: Prefer the Homebrew installation path when available and inspect any shell installer before running it.

## Reference(s):

- [Agented ClawHub skill page](https://clawhub.ai/frane/skills/agented)
- [Agented homepage](https://github.com/frane/agented)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume the ae binary is installed and available on PATH.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
