## Description:

DashClaw platform expert for integration, troubleshooting, and governance. Snapshot-based - prefer live queries via `python -m livingcode query`, or `GET {baseUrl}/api/doctor` when Python/livingcode/the repo are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashclaw](https://clawhub.ai/user/dashclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent integrators use this skill to understand DashClaw's platform shape, troubleshoot integrations, and run diagnostics or validation against a configured DashClaw instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be sent to a user-supplied DashClaw server or exposed through command-line arguments and diagnostic output.

Mitigation: Verify the DashClaw host before running scripts, prefer environment variables over command-line key arguments, use short-lived or least-privileged keys, and avoid sharing diagnostic logs.

Risk: Bootstrap and hook workflows can persist across projects or affect future agent sessions.

Mitigation: Prefer project-scoped installation, review any global hook install before use, and run diagnostics or bootstrap commands in dry-run or read-only mode first when available.

Risk: Full integration validation can create test data on the configured DashClaw instance.

Mitigation: Run read-only validation by default and use full validation only against an intended environment with an appropriate test agent ID.

## Reference(s):

- [DashClaw Platform Intelligence](https://clawhub.ai/dashclaw/skills/dashclaw-platform-intelligence)
- [DashClaw Publisher Profile](https://clawhub.ai/user/dashclaw)
- [DashClaw API Surface](references/api-surface.md)
- [DashClaw Platform Knowledge](references/platform-knowledge.md)
- [DashClaw Troubleshooting Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and optional JSON diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query a live DashClaw API or run bundled Node.js scripts when the user provides a base URL, API key, and target agent workspace.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
