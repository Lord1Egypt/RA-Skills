## Description: <br>
Route AI agent traffic through a residential IP using Tailscale exit nodes - no custom code, no proxies, just WireGuard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicholaslocascio](https://clawhub.ai/user/nicholaslocascio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure a cloud node and a residential node so an AI agent's network traffic exits through a Tailscale residential exit node. It provides setup, verification, isolation, and troubleshooting guidance for that routing pattern. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud or AI-agent traffic may appear to come from the user's residential IP, which can affect privacy, bandwidth, and abuse handling. <br>
Mitigation: Install only for intentional residential egress, prefer a dedicated device or isolated network, monitor bandwidth and abuse reports, and know how to disable the exit node before enabling full-tunnel routing. <br>
Risk: An overly broad exit-node setup can route more traffic through the residential device than intended. <br>
Mitigation: Use Tailscale ACLs and tags to limit which machines can use the exit node, and verify routing with status and IP checks after configuration. <br>
Risk: The setup includes installer commands that fetch software from the internet. <br>
Mitigation: Verify installers and package sources before running them, and review commands before executing them with elevated privileges. <br>


## Reference(s): <br>
- [Claw Relay homepage](https://clawrelay.ai) <br>
- [Tailscale](https://tailscale.com) <br>
- [Tailscale admin console](https://login.tailscale.com/admin/machines) <br>
- [Headscale](https://github.com/juanfont/headscale) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with shell commands, JSON configuration, and short code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the tailscale binary and a Tailscale account or compatible self-hosted control server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
