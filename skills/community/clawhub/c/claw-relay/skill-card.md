## Description:

Route AI agent traffic through a residential IP using Tailscale exit nodes, with no custom code or proxy service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicholaslocascio](https://clawhub.ai/user/nicholaslocascio)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure a residential Tailscale exit node and route a VPS-hosted AI agent's network traffic through that node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routing all VPS agent traffic through a home laptop can make the home connection the visible source of that traffic, creating possible bandwidth, account, reputation, or legal exposure.

Mitigation: Confirm the operator understands the exposure before enabling the exit node, document how to disable the exit node, and verify normal routing can be restored.

Risk: Install commands and network-routing changes can affect host trust and connectivity.

Mitigation: Prefer trusted package-manager installation instructions, review commands before execution, and test routing changes with a controlled workload.

Risk: An unrestricted exit node may allow unintended machines to route traffic through the residential connection.

Mitigation: Use Tailscale ACLs or tags to restrict which machines can use the exit node.

## Reference(s):

- [Claw Relay homepage](https://clawrelay.ai)
- [Tailscale](https://tailscale.com)
- [Tailscale admin console](https://login.tailscale.com/admin/machines)
- [Headscale](https://github.com/juanfont/headscale)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, JSON, Python, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Tailscale CLI on configured nodes and changes network routing when applied.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
