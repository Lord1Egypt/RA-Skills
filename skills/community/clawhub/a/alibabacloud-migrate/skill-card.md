## Description: <br>
Migrate cloud resources from AWS or Azure to Alibaba Cloud by generating a migration assessment report, modular Terraform code, and a step-by-step migration guide; code generation only, with no deployment, data migration, or DNS cutover. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud infrastructure engineers use this skill to assess AWS or Azure infrastructure and generate Alibaba Cloud Terraform plus migration documentation for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect Terraform, tfvars, and tfstate content while preparing migration artifacts. <br>
Mitigation: Run it only in a copied or tightly scoped workspace and review generated artifacts before sharing or applying them. <br>
Risk: Generated Terraform and migration guides could lead to operational cloud changes, paid resource creation, or destructive changes if followed without review. <br>
Mitigation: Do not allow the agent to run terraform apply or destroy; require a human review of plans, costs, DNS changes, workload moves, public endpoints, and source-resource decommissioning. <br>
Risk: The security summary flags weakened approval gating around operational cloud-change guidance. <br>
Mitigation: Require explicit human approval before Terraform generation or execution planning, and treat any pre-approval path as needing separate review before real infrastructure changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-migrate) <br>
- [Discovery and Analysis Workflow](references/workflows/discovery-and-analysis.md) <br>
- [Resource Mapping Workflow](references/workflows/resource-mapping.md) <br>
- [Assessment and Approval Workflow](references/workflows/assessment-report.md) <br>
- [Code Migration Workflow](references/workflows/code-migration.md) <br>
- [Migration Guide Workflow](references/workflows/migration-guide.md) <br>
- [Alibaba Cloud Provider Deprecation Guardrails](references/mappings/alicloud-provider-deprecations.md) <br>
- [AWS Service Mapping Index](references/mappings/aws/index.md) <br>
- [Azure Service Mapping Index](references/mappings/azure/index.md) <br>
- [AWS Terraform Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/{resource}) <br>
- [Alibaba Cloud Terraform Provider Docs](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/{resource}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown, JSON state files, and Terraform configuration files in a .migration-report directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates assessment, mapping, Terraform, validation status, and migration guide artifacts for review before any cloud changes are applied.] <br>

## Skill Version(s): <br>
0.0.1-beta.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
