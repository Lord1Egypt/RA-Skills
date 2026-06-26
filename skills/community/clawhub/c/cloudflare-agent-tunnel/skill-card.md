## Description: <br>
Helps agents configure Cloudflare Tunnel so each OpenClaw agent can be reached through a secure HTTPS hostname without managing certificates, nginx, or public inbound ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to give OpenClaw agents stable HTTPS URLs through Cloudflare Tunnel, including named tunnels, per-agent subdomains, systemd services, DNS routing, and custom domain setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish an OpenClaw agent interface through a persistent Cloudflare hostname without clearly requiring access controls. <br>
Mitigation: Install only when remote access is intended, confirm the exact domain and local port, and enable Cloudflare Access or strong application-level authentication before exposing the endpoint. <br>
Risk: The tunnel runs as a persistent root-managed service and depends on Cloudflare tunnel credentials. <br>
Mitigation: Protect tunnel credentials and document how to stop and disable the systemd service, remove the DNS route, and delete the tunnel when access is no longer needed. <br>


## Reference(s): <br>
- [Custom Domains with Cloudflare Tunnels](references/custom-domains.md) <br>
- [Cloudflare Agent Tunnel on ClawHub](https://clawhub.ai/maverick-software/cloudflare-agent-tunnel) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown with inline bash, JSON, YAML, and systemd configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for cloudflared tunnels, DNS routes, service management, OpenClaw allowed origins, and firewall posture.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
