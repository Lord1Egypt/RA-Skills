## Description: <br>
Guides agents through importing existing Alibaba Cloud resources into Terraform management, including environment checks, authentication, resource discovery, HCL generation, state import, validation, and dependency analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud infrastructure engineers use this skill to bring existing Alibaba Cloud resources under Terraform management for one-time migrations or incremental synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to inspect Alibaba Cloud resources and modify Terraform state. <br>
Mitigation: Use read-only, least-privilege RAM credentials where possible and review every discovery, import, and state command before execution. <br>
Risk: Terraform state and cloud inventory output can contain sensitive infrastructure details. <br>
Mitigation: Keep state and inventory outputs out of public channels and redact sensitive values before sharing. <br>
Risk: The workflow enables aliyun CLI AI-Mode for invocation tracking. <br>
Mitigation: Disable aliyun AI-Mode after the session if it should not remain enabled. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/sdk-team/alibabacloud-terraform-import) <br>
- [Terraform alicloud provider documentation](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs) <br>
- [Terraform installation documentation](https://developer.hashicorp.com/terraform/install) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/document_detail/110244.html) <br>
- [API commands](references/api-commands.md) <br>
- [Dependency rules](references/dependency-rules.md) <br>
- [Incremental sync](references/incremental-sync.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Resource Hub API](references/resource-hub-api.md) <br>
- [Resource types](references/resource-types.md) <br>
- [State management](references/state-management.md) <br>
- [Terraform patterns](references/terraform-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, HCL, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose cloud discovery commands, Terraform configuration, import commands, validation steps, and dependency summaries for user review.] <br>

## Skill Version(s): <br>
0.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
