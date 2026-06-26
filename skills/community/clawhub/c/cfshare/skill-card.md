## Description: <br>
Use the cfshare CLI to expose local ports/files as temporary Cloudflare Quick Tunnel URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ystemsrx](https://clawhub.ai/user/ystemsrx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need a temporary public URL for a local service, file, or directory, or when they need to inspect and export cfshare exposure audit state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local ports or files can become reachable from the internet through temporary Cloudflare links. <br>
Mitigation: Confirm the exact port or file paths before exposing them, use token or basic access for non-public content, and avoid sharing secrets or broad directories. <br>
Risk: Long-lived or forgotten exposures can leave local resources accessible longer than intended. <br>
Mitigation: Use short TTLs, review active exposures, and stop tunnels or file shares when finished. <br>
Risk: Installing required tooling may involve global packages or privileged system commands. <br>
Mitigation: Have the user approve global or privileged installs and verify the required cfshare and cloudflared binaries before use. <br>


## Reference(s): <br>
- [CF Share ClawHub listing](https://clawhub.ai/ystemsrx/cfshare) <br>
- [cloudflared Linux binary release](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64) <br>
- [Cloudflare package repository](https://pkg.cloudflare.com/cloudflared) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI parameters or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return public URLs, expiration times, masked access details, exposure status, logs, and audit records from cfshare commands.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
