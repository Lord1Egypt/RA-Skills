## Description:

Diagnoses Alibaba Cloud ECS public connectivity and VPC cloud service egress issues involving public IP reachability, security groups, NAT, SNAT, routes, and EIPs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use it to diagnose public reachability and outbound connectivity for a specified Alibaba Cloud ECS instance or VPC service, then review the findings and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling can expose secrets.

Mitigation: Use a dedicated read-only identity, ensure credential caches are created safely, redact error output, and verify CLI and SDK calls use the same account.

Risk: Repair guidance could weaken network protections.

Mitigation: Have a network administrator review firewall and access-rule changes, keep exceptions narrow, and restore temporary changes after testing.

Risk: Execution output may include account-balance information.

Mitigation: Limit access to diagnostic results and remove account-balance details before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-ecs-vpc-publicnetwork-troubleshoot)
- [RAM Permission Declaration](references/ram-policies.md)
- [Preparation](references/module1_preparation.md)
- [ECS Public Network Diagnosis](references/module2_ecs_public.md)
- [VPC Cloud Service Public Network Diagnosis](references/module3_vpc_service.md)
- [Output Results and Determination Specification](references/module4_output.md)
- [Solution Guidance](references/module5_solution.md)
- [Alibaba Cloud Security Group Overview](https://help.aliyun.com/zh/ecs/user-guide/security-group-overview)
- [Alibaba Cloud Network ACL Overview](https://help.aliyun.com/zh/vpc/network-acl-overview)
- [Alibaba Cloud VPC Route Tables](https://help.aliyun.com/zh/vpc/vpc-route-table/#e2a77086dae4t)
- [Alibaba Cloud IPv4 Gateway Overview](https://help.aliyun.com/zh/vpc/ipv4-gateway-overview#37b32469c9n6j)
- [Alibaba Cloud Internet NAT Gateway Public Access](https://help.aliyun.com/zh/nat-gateway/user-guide/use-internet-nat-gateway-for-public-network-access)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [JSON diagnostic results and Markdown status tables with remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Resource-scoped, read-only diagnostic results; execution output may include account-balance information.]

## Skill Version(s):

0.0.3 (source: server-resolved release metadata, artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
