## Description:

Automatically detect and renew expired Claude Code OAuth tokens via heartbeat. 3-tier renewal: refresh token -> Chrome browser automation -> user alert.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenhab03](https://clawhub.ai/user/chenhab03)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators running OpenClaw agents with Claude Code use this skill to check OAuth token health during heartbeat cycles, renew credentials when possible, and surface an alert when manual login is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The heartbeat process reads Claude Code credential data from macOS Keychain.

Mitigation: Install only in workspaces where automated Keychain access is acceptable, and review local permissions before enabling the heartbeat check.

Risk: Tier 2 renewal drives Chrome to approve Claude OAuth through Apple Events.

Mitigation: Disable browser automation unless it is needed, and use an isolated Chrome profile when enabling it.

Risk: Security guidance identifies weak consent boundaries and unsafe scripting details.

Mitigation: Require explicit runtime consent, safer temporary-file handling, auth-code validation, and a non-dynamic Expect invocation before routine use.

## Reference(s):

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code GitHub project](https://github.com/anthropics/claude-code)
- [OpenClaw GitHub project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and heartbeat configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script is normally silent when the token is healthy or renewal succeeds, and emits a short OAuth alert when user action is required.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
