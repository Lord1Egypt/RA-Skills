## Description: <br>
Guides agents through creating a whole-instance Alibaba Cloud ECS image and deploying a backup instance in a different availability zone within the same region. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and site reliability engineers use this skill to guide Alibaba Cloud ECS cross-AZ disaster recovery by creating a full-instance image and launching a backup instance while leaving the source instance untouched. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create billable Alibaba Cloud ECS, image, disk, and VSwitch resources. <br>
Mitigation: Confirm the account, region, source instance, target zone, resources to be created, and billing impact before approving execution. <br>
Risk: Broad or long-lived credentials could expose the Alibaba Cloud environment if mishandled. <br>
Mitigation: Use least-privilege RAM roles or temporary credentials and do not paste long-lived access keys into agent commands or chat. <br>
Risk: Incorrect target zone, instance type, disk category, or VSwitch choices could produce an unusable recovery instance. <br>
Mitigation: Use the skill's explicit confirmation prompts and verification steps before each API call and after instance creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-ecs-disaster-recovery-image) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Alibaba Cloud ECS API overview](https://www.alibabacloud.com/help/ecs/developer-reference/api-overview) <br>
- [Alibaba Cloud CLI documentation](https://www.alibabacloud.com/help/cli/what-is-alibaba-cloud-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command blocks and decision prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes explicit user confirmation points, Alibaba Cloud CLI command conventions, permission guidance, and verification checks.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
