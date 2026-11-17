## Description:

Operate and troubleshoot OPNsense and pfSense firewalls, including rules, NAT, VPN, DHCP, diagnostics, and selected configuration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Firewall operators and network engineers use this skill to inspect and troubleshoot OPNsense and pfSense systems, including gateway health, traffic, rules, NAT, VPN, and DHCP. It can also stage and apply selected firewall changes through governed operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-capable credentials allow firewall changes without an enforced approval step, including disruptive high-impact operations.

Mitigation: Use a read-only firewall API account by default, and require explicit operator approval before enabling write access or applying high-impact changes. Review dry-run previews before execution.

Risk: Audit records persist on the local system and may contain operational activity.

Mitigation: Restrict access to the host and audit database, and manage retention under the environment's data-handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zw008/skills/firewall-aiops)
- [Project homepage](https://github.com/AIops-tools/Firewall-AIops)
- [Capabilities reference](artifact/references/capabilities.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [CLI reference](artifact/references/cli-reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown summaries with firewall findings, recommendations, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report live firewall state and describe or carry out selected changes; high-impact operations require careful authorization.]

## Skill Version(s):

0.16.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
