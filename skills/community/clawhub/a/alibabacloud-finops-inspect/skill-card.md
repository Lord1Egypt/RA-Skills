## Description: <br>
Inspects Alibaba Cloud resources across regions to identify idle or underutilized ECS, RDS, EIP, disk, load balancer, and NAT gateway resources and produce cost optimization recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud engineers and FinOps teams use this skill to run a read-only Alibaba Cloud inventory and utilization scan, then review a structured report of idle resources and cost-saving recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Alibaba Cloud inventory, topology, billing attributes, and utilization metrics, and generated reports may include resource IDs, IPs, topology, and workload metrics. <br>
Mitigation: Run it only with a least-privilege read-only RAM user and treat generated reports as sensitive operational data. <br>
Risk: Large-account scans can generate significant read-only API and CloudMonitor call volume. <br>
Mitigation: Use explicit regions and resource types where possible to reduce scan scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-finops-inspect) <br>
- [RAM policies](references/ram-policies.md) <br>
- [API calling patterns](references/api-calling-patterns.md) <br>
- [Related commands](references/related-commands.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Manage Access Credentials in Python](https://help.aliyun.com/zh/sdk/developer-reference/manage-access-credentials) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown/text report with inspection summary, resource detail tables, recommendation summary, and error summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Alibaba Cloud credentials and may include sensitive cloud inventory and utilization details.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
