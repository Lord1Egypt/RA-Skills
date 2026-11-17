## Description:

Provides a standard protocol for delegating work through ACP runtime to acpx-enabled harnesses such as Claude Code, Codex, Gemini CLI, OpenCode, Pi, and Kimi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure ACP delegation workflows, spawn reusable harness sessions, and troubleshoot authentication, permission, and session-return issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends broad automatic authority for delegated external agents, which can permit unintended file changes or command execution.

Mitigation: Prefer read-only or per-task approvals, review the acpx permission configuration before use, and run delegated agents in a restricted workspace.

Risk: API keys may be exposed if credentials are printed in logs or stored in plaintext configuration without protection.

Mitigation: Avoid printing secrets, protect credential files, and use scoped or rotated keys where possible.

Risk: Harness package behavior can change if adapter packages are installed without fixed versions.

Mitigation: Pin harness package versions and review package updates before deploying delegated workflows.

## Reference(s):

- [Harness List](references/harness-list.md)
- [ClawHub Skill Page](https://clawhub.ai/chaoyang78/skills/acp-harness-delegation)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline JavaScript, bash, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational trigger phrases, ACP session spawning guidance, configuration snippets, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
