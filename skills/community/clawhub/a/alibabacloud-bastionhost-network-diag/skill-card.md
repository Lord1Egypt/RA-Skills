## Description:

Diagnoses Alibaba Cloud Bastion Host connection timeouts and access anomalies by checking public-network settings, instance configuration, and Cloud Firewall activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and support engineers use this skill to investigate Bastion Host SSH, RDP, and web access failures and receive a structured diagnosis with next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud queries can expose instance metadata, endpoints, firewall protection state, and traffic-log details.

Mitigation: Use a least-privilege Alibaba Cloud profile with only the listed read-only permissions, and review each displayed command before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-bastionhost-network-diag)
- [Enable O&M over a Private Network](https://help.aliyun.com/zh/bh/bastionhost/user-guide/enable-o-m-over-a-private-network)
- [Bastion Host API examples](references/api-examples.md)
- [Required read-only RAM permissions](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown diagnostic report and chat guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private-domain cases receive manual troubleshooting guidance rather than automatic diagnosis.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
