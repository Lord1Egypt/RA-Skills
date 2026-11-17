## Description:

Manage Alibaba Cloud ECS instances, monitoring, security groups, snapshots, and remote command workflows through agent-guided CLI operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-jiqimao](https://clawhub.ai/user/leo-jiqimao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud ECS resources from an agent workflow, including instance lifecycle actions, metrics lookup, snapshot operations, security-group changes, and remote command execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Alibaba Cloud credentials that can grant broad ECS authority.

Mitigation: Use a least-privilege RAM user, avoid entering long-lived secrets into chat or shell commands, rotate any exposed key, and confirm permissions on ~/.aliyun/config.json.

Risk: Instance stop, reboot, snapshot rollback, and security-group updates can disrupt workloads or expose services.

Mitigation: Manually confirm each high-impact operation before execution, and review any security-group rule that opens access to 0.0.0.0/0.

## Reference(s):

- [ClawHub Aliyun Ecs Skill release](https://clawhub.ai/leo-jiqimao/skills/aliyun-ecs-skill)
- [Alibaba Cloud RAM AccessKey management](https://ram.console.aliyun.com/manage/ak)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that call Alibaba Cloud ECS APIs and change cloud resources.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
