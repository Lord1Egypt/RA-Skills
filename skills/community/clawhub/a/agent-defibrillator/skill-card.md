## Description:

Watchdog that monitors your AI agent gateway and restarts it when it crashes. Triggers on "install defibrillator", "agent watchdog", "gateway monitor", "auto-restart agent", or "keep agent alive". macOS launchd service with optional Discord notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hazy2go](https://clawhub.ai/user/hazy2go)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to install and configure a macOS launchd watchdog that monitors an OpenClaw-style gateway, restarts it after crashes or stale versions, and optionally sends Discord notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can fetch changing remote code and install it as a persistent user-level background service.

Mitigation: Prefer a pinned, reviewed local checkout and remove or disable the install.sh remote download path before installation.

Risk: The README includes a curl-to-bash installation path.

Mitigation: Avoid the curl-to-bash command and review the cloned files before running install.sh.

Risk: The watchdog can restart OpenClaw, terminate matching gateway processes, and send optional Discord messages through the configured OpenClaw CLI.

Mitigation: Install only when that behavior is intended, configure Discord explicitly, and review launchd service settings before enabling the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hazy2go/skills/agent-defibrillator)
- [Agent Defibrillator repository](https://github.com/hazy2go/agent-defibrillator)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces macOS launchd setup, verification, configuration, log inspection, restart, and uninstall instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata, released 2026-02-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
