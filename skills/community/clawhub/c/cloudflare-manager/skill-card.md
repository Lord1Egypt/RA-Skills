## Description: <br>
Manage Cloudflare DNS records, Tunnels (cloudflared), and Zero Trust policies. Use for pointing domains, exposing local services via tunnels, and updating ingress rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Cloudflare DNS records, Cloudflare Tunnel ingress, and selected zone settings for domains and local services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Cloudflare DNS records, zone settings, and local cloudflared ingress. <br>
Mitigation: Use a dedicated least-privilege Cloudflare token scoped to the required zone and permissions. <br>
Risk: Ingress updates can write to /etc/cloudflared/config.yml and restart the cloudflared service with sudo. <br>
Mitigation: Avoid broad sudo access and review local sudo configuration before enabling update-ingress workflows. <br>
Risk: delete-dns, update-setting, and update-ingress actions can make disruptive infrastructure changes. <br>
Mitigation: Run --dry-run first and manually review the planned action before applying changes. <br>


## Reference(s): <br>
- [Cloudflare Manager ClawHub Release](https://clawhub.ai/1999AZZAR/cloudflare-manager) <br>
- [Cloudflare Tunnel Configuration Guide](references/tunnel-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Cloudflare API requests and local cloudflared configuration changes when the user runs the documented commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
