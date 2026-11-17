## Description:

Deploy Alibaba Cloud official tech solutions through Terraform module deployment or CLI step-by-step execution when a user names a solution, shares an Aliyun solution URL, or asks to deploy an official template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to map Alibaba Cloud solution requests to Terraform or CLI execution paths, verify environment and RAM prerequisites, deploy resources, validate results, and produce cleanup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate real Alibaba Cloud infrastructure creation, modification, and destruction.

Mitigation: Use narrowly scoped RAM users or temporary credentials, review plans and estimated costs before apply or destroy actions, and require explicit confirmation before write operations.

Risk: Secrets may be mishandled if passwords, access keys, or tokens are placed directly in Terraform files or CLI commands.

Mitigation: Avoid embedding sensitive values in generated files or command history; provide secrets through approved secure channels and review generated artifacts before execution.

Risk: Evidence reports a shell command injection flaw in state-id handling in the included runtime script.

Mitigation: Treat the runtime script as requiring a security fix before use, avoid untrusted state IDs, and review or patch state-id handling before executing apply, update, or destroy workflows.

Risk: Evidence reports weak handling of downloads and remote diagnostics.

Mitigation: Run diagnostics and downloads only with approved credentials and network context, review outbound requests and returned guidance, and prefer trusted, pinned sources where possible.

## Reference(s):

- [Alibaba Cloud Official Tech Solutions](https://www.aliyun.com/solution/tech-solution)
- [Alibaba Cloud Tech Solutions Catalog](references/alicloud-tech-solutions-all.md)
- [Terraform Solutions Detail](references/tf-plan/tf-solutions.md)
- [Intent Mapping](references/intent-mapping.md)
- [RAM Policies](references/ram-policies.md)
- [Terraform Online Runtime](references/terraform-online-runtime.md)
- [Aliyun CLI Installation Guide](references/aliyun-cli-installation-guide.md)
- [Terraform Defaults](references/terraform-defaults.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, Terraform HCL snippets, execution plans, permission tables, deployment summaries, and cleanup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud resource plans, RAM permission requirements, state IDs, endpoints, and cleanup commands after user confirmation.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
