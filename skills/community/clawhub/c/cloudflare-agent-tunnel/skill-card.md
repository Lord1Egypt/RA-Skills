## Description:

Gives each OpenClaw agent a secure HTTPS URL using Cloudflare Tunnel, covering named tunnels, temporary quick tunnels, multi-agent VPS setup, and custom domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to publish OpenClaw agents running on a VPS through Cloudflare Tunnel with per-agent HTTPS subdomains and local-only origin ports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Cloudflare Tunnel can persistently expose a local OpenClaw service to the internet.

Mitigation: Use it only for intended VPS administration, verify the selected local port, require application authentication or Cloudflare Access, and keep direct origin access blocked.

Risk: The tunnel service examples run cloudflared as root.

Mitigation: Prefer a dedicated non-root cloudflared user with hardened systemd settings before production use.

Risk: Quick tunnels create temporary public URLs that reset and are less suitable for sensitive services.

Mitigation: Use named tunnels for normal deployments and reserve quick tunnels for temporary fallback only.

## Reference(s):

- [Custom Domains with Cloudflare Tunnels](artifact/references/custom-domains.md)
- [Cloudflare Agent Tunnel on ClawHub](https://clawhub.ai/maverick-software/skills/cloudflare-agent-tunnel)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, YAML, and systemd configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include persistent service setup steps for cloudflared and OpenClaw allowedOrigins updates.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
