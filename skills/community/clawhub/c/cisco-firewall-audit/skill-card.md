## Description: <br>
Dual-platform Cisco ASA and Firepower Threat Defense (FTD) firewall audit with ACL analysis, NAT policy validation, Modular Policy Framework / Access Control Policy evaluation, Snort IPS assessment, VPN configuration review, and logging completeness verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network security engineers, firewall administrators, and auditors use this skill to review Cisco ASA and FTD firewall policy posture, including ACLs, NAT, inspection, IPS, VPN, failover, and logging. It is suited to authorized compliance audits, post-incident reviews, and pre-migration baselines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to sensitive firewall configuration, VPN, policy export, and log data. <br>
Mitigation: Use only with explicit authorization, prefer a read-only audit account, and treat collected firewall data as sensitive security information. <br>
Risk: Audit scope that is too broad can expose more firewall domains or devices than intended. <br>
Mitigation: Limit use to named ASA and FTD devices and specific FMC domains approved for the review. <br>


## Reference(s): <br>
- [Cisco ASA and FTD CLI Reference - Audit Commands](references/cli-reference.md) <br>
- [Cisco ASA and FTD Policy Models](references/policy-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Configuration review] <br>
**Output Format:** [Markdown audit guidance with inline shell command blocks and a report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit workflow for authorized Cisco ASA and FTD environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.json release.version and artifact frontmatter metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
