## Description:

OpenClaw Gateway Resilience Guard keeps Gateway, channels, logs, and optional model-provider probes observable after Wi-Fi changes, WSL sleep/resume, session expiry, provider timeouts, or partial outages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zc-kama](https://clawhub.ai/user/zc-kama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and run a persistent local watchdog for OpenClaw Gateway, channel health, diagnostics, and recovery workflows on Linux, WSL, macOS, or Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog installs persistent user-level services and can restart OpenClaw Gateway.

Mitigation: Install only when persistent local monitoring is intended, review the generated service or scheduled task, and keep restart limits enabled.

Risk: Dashboard token and command settings create local command-execution exposure if actions or custom commands are enabled without review.

Mitigation: Keep the dashboard bound to 127.0.0.1, avoid custom command settings, disable dashboard actions where possible, and protect config and state directories.

Risk: Diagnostics and exported logs can expose local paths, operational details, channel URLs, or provider metadata.

Mitigation: Review diagnostic exports and logs before sharing them outside the local operator environment.

## Reference(s):

- [OpenClaw Gateway Resilience Guard on ClawHub](https://clawhub.ai/zc-kama/skills/gateway-resilience-guard)
- [Tencent/openclaw-weixin issue 141](https://github.com/Tencent/openclaw-weixin/issues/141)
- [Tencent/openclaw-weixin issue 155](https://github.com/Tencent/openclaw-weixin/issues/155)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with shell, PowerShell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator guidance for installing, configuring, monitoring, and uninstalling the watchdog and optional OpenClaw plugin bridge.]

## Skill Version(s):

1.4.4 (source: server evidence release metadata, CHANGELOG, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
