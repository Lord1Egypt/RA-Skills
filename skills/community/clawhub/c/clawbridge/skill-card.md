## Description:

ClawBridge provides a mobile-first dashboard for OpenClaw agents, including real-time activity monitoring, token cost tracking, cron task control, and optional Cloudflare Tunnel remote access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamwing](https://clawhub.ai/user/dreamwing)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use ClawBridge to monitor OpenClaw agent activity from a phone, review token costs, and trigger scheduled tasks through a local dashboard. Teams may optionally expose the dashboard remotely through a Cloudflare Tunnel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation executes an unverified remote script under the user's account.

Mitigation: Review the installer before running it and prefer a pinned, verifiable release.

Risk: The persistent dashboard service can become internet-reachable when Cloudflare Tunnel or Quick Tunnel is enabled.

Mitigation: Enable remote access only when needed, protect the generated access key, and confirm how to stop and remove the user-level systemd service.

## Reference(s):

- [ClawBridge ClawHub listing](https://clawhub.ai/dreamwing/skills/clawbridge)
- [ClawBridge homepage](https://clawbridge.app)
- [ClawBridge README](https://github.com/dreamwing/clawbridge/blob/master/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces install, update, service-management, authentication, and optional tunnel setup guidance for a local Node.js dashboard.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact SKILL.md declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
