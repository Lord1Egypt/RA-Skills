## Description: <br>
Manage the full lifecycle of Alibaba Cloud PAI DSW (Data Science Workshop) instances, including create, update, query, list, start, stop, and ECS spec lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud PAI DSW notebook/workspace instances through Aliyun CLI workflows while confirming account, region, workspace, compute, image, and lifecycle parameters before action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud lifecycle actions can create, update, start, or stop cost-impacting PAI DSW resources. <br>
Mitigation: Use the skill only for intended Alibaba Cloud PAI DSW management, and explicitly confirm region, workspace, instance ID, compute spec, image, cost impact, and active work before create, update, start, or stop operations. <br>
Risk: Alibaba Cloud credentials or access keys could be mishandled during setup. <br>
Mitigation: Use a least-privilege RAM user or temporary credentials, configure credentials outside chat or command lines, and check credential status with `aliyun configure list` without exposing secret values. <br>
Risk: Insufficient or overly broad RAM permissions can block operations or expand account exposure. <br>
Mitigation: Review the documented minimum-permission policy before use and pause on permission errors until the required RAM grants are confirmed. <br>
Risk: Incorrect region, ECS spec, image type, or dataset mount choices can cause failed starts or unintended resource configuration. <br>
Mitigation: Verify spec availability in the target region, match CPU/GPU image type to compute spec, and require explicit user confirmation for all dataset and user-customizable parameters. <br>


## Reference(s): <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Common Images](references/common-images.md) <br>
- [PAI DSW API Overview](https://help.aliyun.com/zh/pai/developer-reference/api-pai-dsw-2022-01-01-overview) <br>
- [Create and Manage Workspaces](https://help.aliyun.com/zh/pai/user-guide/create-and-manage-workspaces) <br>
- [Create a DSW Instance Image](https://help.aliyun.com/zh/pai/user-guide/create-a-dsw-instance-image) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-pai-dsw-manage) <br>
- [Publisher Profile](https://clawhub.ai/user/sdk-team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Aliyun CLI commands that require authenticated Alibaba Cloud access and explicit confirmation before cost-impacting lifecycle actions.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
