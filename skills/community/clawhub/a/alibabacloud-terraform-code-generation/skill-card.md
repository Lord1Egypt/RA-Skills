## Description: <br>
Generates validated Terraform HCL for Alibaba Cloud infrastructure by consulting current aliyun/alicloud provider documentation, local resource catalogs, and deprecation guidance before writing project files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to turn natural-language Alibaba Cloud infrastructure requirements into Terraform HCL, with catalog checks, provider documentation lookups, deprecation audits, and validation summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Terraform could create or modify Alibaba Cloud infrastructure if a user applies it outside the skill. <br>
Mitigation: Review generated Terraform before applying it, and keep terraform apply as a separate user-controlled action. <br>
Risk: Opt-in terraform plan can use existing Alibaba Cloud credentials configured in the environment. <br>
Mitigation: Request terraform plan only when credential-backed planning is intended, and do not paste access keys into prompts or HCL. <br>


## Reference(s): <br>
- [Alibaba Cloud Terraform provider catalog](references/alicloud-providers.md) <br>
- [Auth and network reference](references/auth-and-network.md) <br>
- [Deprecated fields reference](references/deprecated-fields.md) <br>
- [Product-specific resource patterns](references/resource-patterns.md) <br>
- [Terraform Registry aliyun/alicloud provider versions](https://registry.terraform.io/v1/providers/aliyun/alicloud/versions) <br>
- [Terraform Registry aliyun/alicloud latest provider](https://registry.terraform.io/providers/aliyun/alicloud/latest) <br>
- [aliyun/terraform-provider-alicloud releases](https://github.com/aliyun/terraform-provider-alicloud/releases) <br>
- [Alibaba Cloud Terraform init acceleration configuration](https://help.aliyun.com/zh/terraform/terraform-init-acceleration-solution-configuration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown response with Terraform HCL, shell command snippets, file paths, and validation status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write Terraform .tf files to a requested project directory and may run terraform fmt, init, validate, or opt-in plan checks when available.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
