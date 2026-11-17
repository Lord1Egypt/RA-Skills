## Description:

Shares local development servers through a self-hosted frp tunnel with custom domains and automatic HTTPS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darwin7381](https://clawhub.ai/user/darwin7381)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and operate a self-hosted frp, Caddy, Cloudflare DNS, and VPS tunnel for sharing local development services over HTTPS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent long-lived privileged access to a VPS.

Mitigation: Use a non-root VPS user with limited sudo, avoid passphrase-free root keys, and keep SSH access scoped to the tunnel host.

Risk: The setup exposes internet-facing services and an frp dashboard.

Mitigation: Restrict or disable the dashboard, expose only services intended for public access, and verify each tunnel before sharing its URL.

Risk: Downloaded binaries and DNS credentials are part of the setup path.

Mitigation: Verify downloaded binaries before installation and store the Cloudflare token with stricter file permissions or systemd credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darwin7381/skills/frp-tunnel)
- [Setup guide](artifact/setup-guide.md)
- [frp releases](https://github.com/fatedier/frp/releases)
- [Hetzner Cloud](https://www.hetzner.com/cloud/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational checks for tunnel availability and VPS troubleshooting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
