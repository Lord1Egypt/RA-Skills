## Description:

Manage your doxx.net private network: tunnels, devices, firewall, domains, DNS blocking, IP addresses, profiles, account settings, bandwidth stats, and security alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doxxnet](https://clawhub.ai/user/doxxnet)

### License/Terms of Use:

MIT-0

## Use Case:

External users and network administrators use this skill to inspect and manage doxx.net private-network resources, including tunnels, domains, DNS blocking, firewall rules, devices, addresses, tokens, account settings, and network statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad doxx.net account and network-administration authority.

Mitigation: Use a short-lived, least-privilege token with IP restrictions, and avoid admin tokens unless the requested task requires them.

Risk: Token, recovery-code, domain, firewall, device, and tunnel actions can expose or alter sensitive account and network state.

Mitigation: Do not print or store full tokens or recovery codes in chat, and review destructive or privilege-changing actions before execution.

Risk: The skill relies on mutable remote API documentation and live endpoint behavior.

Mitigation: Check the live API manifest and response status fields before acting, and treat HTTP 200 responses as potentially unsuccessful until the body confirms success.

Risk: WireGuard configurations and QR generation can involve private keys.

Mitigation: Prefer local QR generation for WireGuard configs instead of sending private-key material to a remote QR endpoint.

## Reference(s):

- [doxxnet ClawHub page](https://clawhub.ai/doxxnet/skills/doxxnet)
- [doxxnet publisher profile](https://clawhub.ai/user/doxxnet)
- [doxx skills homepage](https://github.com/doxxcorp/doxx-skills)
- [doxx.net live configuration manifest](https://config.doxx.net/)
- [Manage doxx.net Account](references/manage-account.md)
- [Manage doxx.net Addresses & Profiles](references/manage-addresses.md)
- [Manage doxx.net Devices](references/manage-devices.md)
- [Manage doxx.net DNS Blocking](references/manage-dns-blocking.md)
- [Manage doxx.net Domains](references/manage-domains.md)
- [Manage doxx.net Firewall](references/manage-firewall.md)
- [Manage doxx.net Tokens](references/manage-tokens.md)
- [Manage doxx.net Tunnels](references/manage-tunnels.md)
- [doxx.net Network Stats](references/network-stats.md)
- [doxx.net Network Status](references/network-status.md)
- [doxx.net Network Wizard](references/network-wizard.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, tables, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce curl commands, WireGuard configuration guidance, local QR generation guidance, and account or network-management recommendations.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
