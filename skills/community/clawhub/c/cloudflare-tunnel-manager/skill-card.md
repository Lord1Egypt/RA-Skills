## Description: <br>
Create and manage secure Cloudflare Tunnels using cloudflared to expose local services, configure DNS routing, set up zero-trust access controls, and manage tunnel authentication without opening firewall ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qoohsuan](https://clawhub.ai/user/qoohsuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and operators use this skill to plan and run Cloudflare Tunnel workflows for exposing local web, API, TCP, SSH, and administrative services without opening inbound firewall ports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tunnel examples can expose local services to the internet if hostnames, routes, or ports are applied without review. <br>
Mitigation: Confirm the active Cloudflare account and zone, review each hostname and local port, and protect admin, SSH, and file endpoints with Cloudflare Access before running commands. <br>
Risk: Cloudflare Tunnel credential JSON files and service tokens can grant access to private infrastructure. <br>
Mitigation: Treat ~/.cloudflared JSON files and service tokens like private keys, avoid sharing them, and back them up only to protected locations. <br>
Risk: Disabling TLS verification can hide origin certificate problems. <br>
Mitigation: Use noTLSVerify only for temporary debugging and restore certificate validation before production use. <br>


## Reference(s): <br>
- [cloudflared Linux AMD64 release download](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64) <br>
- [Cloudflare Tunnel Manager on ClawHub](https://clawhub.ai/qoohsuan/cloudflare-tunnel-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell, YAML, INI, XML, and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples, tunnel configuration snippets, service setup files, and operational guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: clawhub.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
