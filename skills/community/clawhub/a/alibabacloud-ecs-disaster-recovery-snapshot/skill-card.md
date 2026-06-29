## Description: <br>
Guides agents through Alibaba Cloud ECS snapshot-based cross-AZ disaster recovery backups, including full-instance recovery to another availability zone and disk-level recovery to an existing target instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to plan and execute Alibaba Cloud ECS backup and recovery workflows with Aliyun CLI commands, user confirmations, RAM permission guidance, and completion summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create billable Alibaba Cloud resources such as ECS snapshots, images, disks, VSwitches, and recovery instances. <br>
Mitigation: Use a tightly scoped RAM user or role, prefer STS or ECS RAM roles, and confirm the target region, availability zone, resource IDs, and cost-impacting changes before execution. <br>
Risk: Incorrect resource identifiers or target locations could produce recovery resources in the wrong place. <br>
Mitigation: Confirm all user-customizable parameters, including region, availability zone, source instance, target instance, and disk IDs, before running API-changing commands. <br>
Risk: Credential exposure could increase Alibaba Cloud account risk. <br>
Mitigation: Follow the skill credential-safety rules: do not read, print, enter, export, or set AK/SK values in the agent session; use existing Aliyun CLI credential configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-ecs-disaster-recovery-snapshot) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Error Handling Guide](references/error-handling.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [ECS API Reference](https://www.alibabacloud.com/help/ecs/developer-reference/api-overview) <br>
- [Aliyun CLI Documentation](https://www.alibabacloud.com/help/cli/what-is-alibaba-cloud-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and operation summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-confirmed Alibaba Cloud region, availability zone, instance, disk, and credential state before API-changing commands.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
