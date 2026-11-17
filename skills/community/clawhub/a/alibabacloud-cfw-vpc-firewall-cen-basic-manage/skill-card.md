## Description:

Helps operators inspect and manage Alibaba Cloud Firewall VPC border firewalls on CEN Basic Edition, including VPC attachment, traffic diversion, removal, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and engineers use this skill to inventory and troubleshoot CEN Basic Edition VPC firewall slots and to attach VPCs, change diversion, rename firewalls, or remove access with explicit confirmation for disruptive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firewall changes can disrupt production traffic or remove shared regional firewall resources.

Mitigation: Review the exact target and impact, and obtain explicit operator confirmation before switching diversion or removing access.

Risk: Overprivileged credentials or unverified CLI installation sources increase operational exposure.

Mitigation: Review RAM permissions, use least-privilege credentials, and verify CLI and plugin installation sources before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-cfw-vpc-firewall-cen-basic-manage)
- [Basic Edition VPC firewall configuration](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/user-guide/configure-a-vpc-firewall-for-a-basic-edition-transit-router)
- [Cloud Firewall RAM permissions](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/developer-reference/api-cloudfw-2017-12-07-ram)
- [Operational workflow](references/workflow.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON status results]

**Output Format:** [Markdown guidance and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Alibaba Cloud CLI, Cloud Firewall plugin, and authorized credentials for live operations.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
