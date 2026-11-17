## Description:

Practical playbook for running agents through acpx in persistent sessions for reliable file creation, local installs, shell-based writes, structured deliverables, and multi-step coding work across Claude, Codex, Pi, Gemini, OpenCode, and other ACP-compatible agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operators use this skill to choose and run ACPX-managed agent sessions for file-producing, artifact-generating, and multi-step delivery workflows. It is especially useful when prior ACPX attempts failed because of permission settings, shell quoting, sandbox boundaries, CLI differences, or agent reliability issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes broad ACPX session permissions and approve-all style configuration changes.

Mitigation: Start with read-only or auto modes where practical, avoid persistent approve-all settings unless intentionally needed, and restore narrower permissions after the task.

Risk: Shell or Python write fallbacks can create or overwrite files in unexpected locations if output paths are ambiguous.

Mitigation: Confirm exact output paths before file writes, generate fragile artifacts under /tmp first, validate them, and copy them to the final workspace only after validation.

Risk: Local package installs may introduce unpinned dependencies or fail under restricted hosts.

Mitigation: Prefer project-local virtual environments, pin or verify packages before installation, and use stdlib-only fallback paths when dependency installation is unavailable.

Risk: Agent and provider reliability can drift because of authentication, quota, relay, permission, or CLI-shape changes.

Mitigation: Use the verification ladder of fixed-text response, minimal file write, and one real artifact task before trusting an agent for delivery work.

## Reference(s):

- [ACPX Agent Playbook on ClawHub](https://clawhub.ai/spyfree/skills/acpx-agent-playbook)
- [Agent Matrix](references/agent-matrix.md)
- [Provider and Agent Compatibility Notes](references/provider-compat.md)
- [ACPX Troubleshooting Notes](references/troubleshooting.md)
- [PPT Playbook for ACPX Agents](references/ppt-playbook.md)
- [Migration Notes](references/migration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and reusable prompt snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational recommendations and validation checklists rather than executable automation.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
