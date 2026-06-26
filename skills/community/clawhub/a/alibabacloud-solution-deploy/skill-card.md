## Description: <br>
Deploys Alibaba Cloud official tech solutions by routing requests through Terraform module deployment or CLI-first execution paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to plan, confirm, execute, and verify Alibaba Cloud solution deployments. It helps choose between official Terraform modules and CLI workflows, including environment checks, RAM permission review, resource creation, and cleanup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or delete Alibaba Cloud resources that may incur cost or cause irreversible changes. <br>
Mitigation: Use a dedicated least-privilege RAM user or role, review every proposed plan before apply or destroy, and keep the generated cleanup and state information. <br>
Risk: The remote diagnostic helper may send full failed commands and error output to a diagnostic API. <br>
Mitigation: Avoid pasting real secrets into commands or chat transcripts, and redact commands and error output before using the diagnostic helper. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-solution-deploy) <br>
- [Alibaba Cloud Tech Solutions Catalog](references/alicloud-tech-solutions-all.md) <br>
- [Aliyun CLI Installation Guide](references/aliyun-cli-installation-guide.md) <br>
- [Intent Mapping](references/intent-mapping.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Terraform Online Runtime](references/terraform-online-runtime.md) <br>
- [Terraform Solutions Detail](references/tf-plan/tf-solutions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Terraform configuration, command output summaries, and deployment plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud resource IDs, endpoints, state IDs, cleanup commands, and permission checklists.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
