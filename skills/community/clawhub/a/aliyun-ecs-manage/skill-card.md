## Description:

Use when managing Alibaba Cloud Elastic Compute Service (ECS) via OpenAPI/SDK, including listing or creating instances, starting/stopping/rebooting, managing disks/snapshots/images/security groups/key pairs/ENIs, querying status, and troubleshooting workflows for this product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and operations engineers use this skill to administer Alibaba Cloud ECS resources through official OpenAPI and SDK workflows. It supports inventory, lifecycle actions, storage, snapshots, images, security groups, network interfaces, monitoring queries, and Cloud Assistant command execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help perform destructive ECS operations such as stopping, deleting, resizing, or modifying cloud resources.

Mitigation: Use narrowly scoped RAM roles and require human review of target regions, resource identifiers, and requested lifecycle actions before execution.

Risk: The skill includes Cloud Assistant remote command execution, which can run shell or PowerShell commands on ECS instances.

Mitigation: Avoid broad RunCommand permissions unless needed and review every command, instance target, and collected command output before and after execution.

Risk: Generated inventory and command-output files may contain sensitive cloud resource details.

Mitigation: Store outputs under the documented output directory with appropriate access controls and treat saved evidence as sensitive operational data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-ecs-manage)
- [ECS OpenAPI Overview](artifact/references/api_overview.md)
- [ECS OpenAPI Endpoints](artifact/references/endpoints.md)
- [DescribeInstances](artifact/references/describe-instances.md)
- [ECS Cloud Assistant RunCommand](artifact/references/command-assistant.md)
- [ECS Instances](artifact/references/instances.md)
- [ECS Security Groups](artifact/references/security-groups.md)
- [ECS Disks](artifact/references/disks.md)
- [ECS Snapshots](artifact/references/snapshots.md)
- [Source Reference Links](artifact/references/sources.md)
- [Official ECS API Operation List](https://www.alibabacloud.com/help/en/ecs/developer-reference/api-ecs-2014-05-26-overview)
- [Official RunCommand API](https://www.alibabacloud.com/help/en/ecs/developer-reference/runcommand)
- [Official DescribeInstances API](https://www.alibabacloud.com/help/en/ecs/developer-reference/describeinstances)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with Python SDK examples, shell commands, and JSON or TSV evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommended generated evidence is saved under output/aliyun-ecs-manage/ and may include sensitive cloud inventory or command-output data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
