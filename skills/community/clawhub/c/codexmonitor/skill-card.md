## Description:

List, inspect, and watch local OpenAI Codex sessions from the CLI and VS Code using the CodexMonitor Homebrew formula.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

Developers and engineers on macOS use this skill to install and run CodexMonitor for listing, inspecting, and watching local OpenAI Codex CLI or VS Code session logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party binary.

Mitigation: Review the CodexMonitor source and Homebrew formula before installing.

Risk: CodexMonitor reads sensitive local Codex session history.

Mitigation: Treat Codex session logs as confidential and use the narrowest practical session directory.

Risk: Session paths may be redirected through CODEX_SESSIONS_DIR or CODEX_HOME.

Mitigation: Avoid pointing those variables at shared or synced locations.

Risk: Long-running watch mode can continue observing new session content.

Mitigation: Do not leave watch running longer than needed.

## Reference(s):

- [Codexmonitor ClawHub listing](https://clawhub.ai/odrobnik/skills/codexmonitor)
- [CodexMonitor project homepage](https://github.com/Cocoanetics/CodexMonitor)
- [SETUP.md](artifact/SETUP.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports list, show, and watch workflows for local Codex session files.]

## Skill Version(s):

0.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
