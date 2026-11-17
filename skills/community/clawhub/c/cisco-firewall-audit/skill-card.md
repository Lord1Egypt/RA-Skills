## Description:

Dual-platform Cisco ASA and Firepower Threat Defense (FTD) firewall audit with ACL analysis, NAT policy validation, Modular Policy Framework / Access Control Policy evaluation, Snort IPS assessment, VPN configuration review, and logging completeness verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network security engineers, firewall administrators, and compliance reviewers use this skill to perform read-only Cisco ASA and FTD firewall policy audits, including ACL, NAT, inspection, IPS, VPN, failover, and logging checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firewall configuration, VPN details, tokens, and logs collected during an audit may contain sensitive network security data.

Mitigation: Use authorized read-only accounts where possible, avoid configuration mode, and handle collected outputs as sensitive data.

Risk: Audit guidance may be misapplied to firewalls outside the operator's authorization or change-control scope.

Mitigation: Install and use the skill only for Cisco firewalls the operator is explicitly authorized to audit.

## Reference(s):

- [Cisco ASA and FTD CLI Reference - Audit Commands](references/cli-reference.md)
- [Cisco ASA and FTD Policy Models](references/policy-model.md)
- [ClawHub skill page](https://clawhub.ai/vahagn-madatyan/skills/cisco-firewall-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with read-only command blocks and structured audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; command execution should use authorized read-only Cisco ASA, FTD, FMC, FDM, SSH, console, or web/API access.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
