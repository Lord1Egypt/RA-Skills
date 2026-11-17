## Description:

Agentic AI-native multi-tier DNS routing, live packet tracing, and failover bypass engine for Pi-hole, CoreDNS, dnsdist, Unbound, Stubby, DNSCrypt-Proxy, and VPN DNS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dedsecorg](https://clawhub.ai/user/dedsecorg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network operators use this skill to inspect DNS service status, resolve test queries, trace packets, manage dnsdist routes, bypass failing resolvers, query Pi-hole logs, and configure REST or MCP access for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DNS routing, failover, and encrypted DNS enforcement commands can disrupt name resolution or change firewall behavior.

Mitigation: Use only in environments where DNS and firewall changes are intentional; require review of exact rules, privileges, confirmation prompts, rollback or cleanup behavior, and UDP/443 blocking limits before allowing mutating commands to run.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/dedsecorg/agentic-dns/tree/main/skills/agentic-dns)
- [ClawHub skill page](https://clawhub.ai/dedsecorg/skills/agentic-dns)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational commands that mutate DNS routing or firewall behavior; review before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
