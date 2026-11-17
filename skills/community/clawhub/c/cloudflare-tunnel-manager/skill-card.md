## Description:

Create and manage secure Cloudflare Tunnels using cloudflared, including DNS routing, Zero Trust access controls, and tunnel authentication without opening firewall ports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qoohsuan](https://clawhub.ai/user/qoohsuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to set up and manage Cloudflare Tunnels, DNS routes, Zero Trust access controls, and service startup examples for exposing local HTTP, TCP, SSH, API, or admin services through Cloudflare without opening inbound firewall ports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tunnel examples can create long-lived public exposure for local, admin, API, SSH, or development services.

Mitigation: Require Cloudflare Access and application authentication before exposing sensitive services, validate every ingress route, and run tunnels interactively before enabling persistent services.

Risk: The examples include noTLSVerify and an unpinned latest binary download, which can weaken transport verification or installation repeatability.

Mitigation: Use noTLSVerify only for tightly controlled local testing and prefer verified package-manager installation or pinned cloudflared release artifacts.

Risk: Systemd, LaunchAgent, and credential backup examples can leave persistent tunnel access or copied ~/.cloudflared credentials in place.

Mitigation: Do not enable persistence until rollback is planned, and protect or rotate cloudflared credential files and backups.

## Reference(s):

- [Cloudflare Tunnel Manager on ClawHub](https://clawhub.ai/qoohsuan/skills/cloudflare-tunnel-manager)
- [cloudflared Linux release download](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, YAML, INI, XML, and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides command and configuration examples for cloudflared tunnel setup, routing, persistence, monitoring, backup, and migration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
