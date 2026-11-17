## Description:

Manage Clash VPN proxy service for accessing blocked websites like Google Play. Use when the user needs to (1) setup/configure VPN proxy, (2) update Clash proxy configuration, (3) start/stop VPN service, (4) test proxy connectivity, or (5) access blocked resources through proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxnan](https://clawhub.ai/user/lxnan)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure, start, stop, restart, inspect, and test a Clash proxy service, including updating Clash configuration content and using local proxy endpoints for blocked resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network-facing Clash defaults can expose controller, DNS, or LAN-accessible proxy behavior beyond the local host.

Mitigation: Bind controller and DNS endpoints to localhost or a trusted interface, add a controller secret, and avoid enabling LAN access unless it is explicitly needed.

Risk: Root-owned configuration updates and service restarts can overwrite working Clash settings or disrupt connectivity.

Mitigation: Back up existing configuration, validate new configuration in a temporary path before replacement, and review commands before execution.

## Reference(s):

- [Clash VPN configuration guide](references/config-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that modify root-owned Clash configuration and control the local proxy service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
