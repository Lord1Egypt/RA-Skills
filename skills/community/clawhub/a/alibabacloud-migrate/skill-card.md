## Description:

Migrate cloud resources from AWS/Azure to Alibaba Cloud by producing a migration assessment report, modular Terraform code, and a step-by-step migration guide without performing deployment, data migration, or DNS cutover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to assess AWS or Azure infrastructure and generate Alibaba Cloud Terraform, mapping artifacts, and migration guidance. It supports planning and infrastructure-as-code generation, while leaving execution and production rollout decisions to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy sensitive Terraform state data and variable values into local plaintext reports.

Mitigation: Use it only in workspaces where Terraform state and variable files may be read, keep .migration-report/ private and out of source control, and inspect generated reports for secrets before sharing.

Risk: The skill may interact with the local environment more than expected for a code-generation workflow.

Mitigation: Review the skill before installing it in sensitive infrastructure repositories and expect Terraform validation to run locally with possible provider or plugin network access.

Risk: Generated Terraform can introduce risky infrastructure changes, including public endpoints or unwanted preapproval behavior.

Mitigation: Review generated Terraform carefully, especially public exposure and approval handling, before applying any plan.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-migrate)
- [Phase 1: Discovery and Analysis](references/workflows/discovery-and-analysis.md)
- [Phase 2: Resource Mapping](references/workflows/resource-mapping.md)
- [Phase 3: Assessment & Approval](references/workflows/assessment-report.md)
- [Phase 4: Generate Terraform Code](references/workflows/code-migration.md)
- [Phase 5: Generate Migration Guide](references/workflows/migration-guide.md)
- [Alibaba Cloud Provider Deprecation Guardrails](references/mappings/alicloud-provider-deprecations.md)
- [AWS Service to Alibaba Cloud Mapping Index](references/mappings/aws/index.md)
- [AWS Compute Services to Alibaba Cloud Mapping](references/mappings/aws/compute.md)
- [AWS Networking Services to Alibaba Cloud Mapping](references/mappings/aws/networking.md)
- [AWS Security Services to Alibaba Cloud Mapping](references/mappings/aws/security.md)
- [AWS Storage Services to Alibaba Cloud Mapping](references/mappings/aws/storage.md)
- [Azure Service to Alibaba Cloud Mapping Index](references/mappings/azure/index.md)
- [Azure Compute Services to Alibaba Cloud Mapping](references/mappings/azure/compute.md)
- [Azure Database Services to Alibaba Cloud Mapping](references/mappings/azure/database.md)
- [Azure Networking Services to Alibaba Cloud Mapping](references/mappings/azure/networking.md)
- [HashiCorp AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [HashiCorp AzureRM Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Alibaba Cloud Terraform Provider Documentation](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown reports and guides, JSON state and mapping files, and Terraform HCL files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a .migration-report/ workspace with assessment, migration state, parsed resource data, Terraform modules, and deployment guidance.]

## Skill Version(s):

0.0.1-beta.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
