## Description: <br>
Identify and reduce AWS data transfer costs across inter-region, cross-AZ, internet egress, and NAT Gateway traffic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, cloud engineers, and FinOps teams use this skill to analyze AWS data transfer spend, identify costly traffic patterns, estimate savings, and produce Terraform configuration for recommended VPC Endpoint changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS billing, flow-log, and architecture data may contain sensitive operational details. <br>
Mitigation: Provide only the billing, flow-log, and architecture data needed for the cost analysis. <br>
Risk: Generated Terraform can change network routing or service access if applied without review. <br>
Mitigation: Have an AWS networking owner review generated Terraform before applying it. <br>
Risk: The skill references shell use through its tool metadata. <br>
Mitigation: Explicitly approve any shell command before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anmolnagpal/data-transfer-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with cost breakdowns, ROI tables, and Terraform configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ready-to-apply VPC Endpoint Terraform for top optimization candidates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
