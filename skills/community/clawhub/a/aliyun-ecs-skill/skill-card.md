## Description: <br>
Manage Alibaba Cloud ECS (Elastic Compute Service) by querying instances, monitoring metrics, managing security groups and snapshots, and executing remote commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-jiqimao](https://clawhub.ai/user/leo-jiqimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external OpenClaw users use this skill to administer Alibaba Cloud ECS resources from an agent workflow, including instance lifecycle operations, monitoring, snapshot handling, firewall rules, and remote command execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Alibaba Cloud ECS resources using powerful credentials. <br>
Mitigation: Use a dedicated RAM user with minimal permissions and avoid placing long-lived AccessKey secrets in logged chat or shell commands. <br>
Risk: Stop, restart, snapshot rollback, deletion, and security-group changes can cause outages, data loss, or unintended public exposure. <br>
Mitigation: Require exact region and resource IDs, obtain explicit confirmation before critical actions, and provide restrictive CIDR ranges for firewall rules. <br>
Risk: Stored Alibaba Cloud credentials may remain usable if exposed. <br>
Mitigation: Verify permissions on ~/.aliyun/config.json and rotate any exposed AccessKey credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leo-jiqimao/aliyun-ecs-skill) <br>
- [Publisher profile](https://clawhub.ai/user/leo-jiqimao) <br>
- [Alibaba Cloud AccessKey management](https://ram.console.aliyun.com/manage/ak) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce operational guidance for Alibaba Cloud ECS resources and command examples that require user-provided region, resource IDs, and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
