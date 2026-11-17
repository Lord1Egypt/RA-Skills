## Description:

Cursor Agent CLI integration - AI-powered coding agent for terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kailian](https://clawhub.ai/user/kailian)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to run Cursor Agent CLI for terminal-based coding assistance, including planning, code review, refactoring, test generation, documentation, and CI-oriented analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents a pipe-to-shell installer for Cursor Agent CLI.

Mitigation: Independently verify the official installer and source before execution, or use an installation method approved by the deployment environment.

Risk: Cursor Agent CLI can modify files, run commands, persist sessions, and run in cloud/background execution.

Mitigation: Use plan or ask mode first, review proposed changes before approval, and limit use to trusted workspaces.

Risk: High-authority flags such as --force, --yolo, --trust, or disabled sandboxing can reduce review and isolation.

Mitigation: Avoid these flags on untrusted code and keep sandboxing enabled unless there is a reviewed operational need.

Risk: API keys may be exposed through command history, logs, or scripts.

Mitigation: Use approved secret handling and avoid placing CURSOR_API_KEY values directly in shell commands or committed files.

## Reference(s):

- [Cursor CLI Overview](https://cursor.com/docs/cli/overview)
- [Cursor Agents](https://cursor.com/agents)
- [Cursor Community Forum](https://forum.cursor.com)
- [ClawHub Skill Page](https://clawhub.ai/kailian/skills/cursor-agent-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and optional JSON output from Cursor Agent CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Cursor Agent CLI binaries `agent` and `cursor`; optional workflows may use `git` or `gh`.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
