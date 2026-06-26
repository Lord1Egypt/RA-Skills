## Description: <br>
Use when managing Alibaba Cloud Elastic Compute Service (ECS) via OpenAPI/SDK, including listing or creating instances, starting/stopping/rebooting, managing disks/snapshots/images/security groups/key pairs/ENIs, querying status, and troubleshooting workflows for this product. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and SREs use this skill to manage Alibaba Cloud ECS resources through SDK-backed workflows, including inventory, lifecycle actions, monitoring queries, and operational troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run arbitrary commands on Alibaba Cloud ECS instances when active cloud credentials are available. <br>
Mitigation: Require explicit human approval before remote command execution, especially for production instances. <br>
Risk: Broad RAM permissions can allow lifecycle, disk, snapshot, image, security-group, and remote-command changes beyond the intended task. <br>
Mitigation: Use temporary or least-privilege RAM credentials, and prefer read-only credentials for inventory workflows. <br>
Risk: Operational changes to ECS resources can affect availability, data retention, or network exposure. <br>
Mitigation: Review every lifecycle, disk, snapshot, image, and security-group action before execution and verify results with describe/list APIs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-ecs-manage) <br>
- [ECS OpenAPI overview](references/api_overview.md) <br>
- [ECS OpenAPI endpoints](references/endpoints.md) <br>
- [DescribeInstances (ECS)](references/describe-instances.md) <br>
- [ECS Cloud Assistant (RunCommand)](references/command-assistant.md) <br>
- [ECS instances](references/instances.md) <br>
- [ECS disks (EBS)](references/disks.md) <br>
- [ECS snapshots](references/snapshots.md) <br>
- [ECS images](references/images.md) <br>
- [ECS security groups](references/security-groups.md) <br>
- [ECS network interfaces (ENI)](references/network-interfaces.md) <br>
- [ECS key pairs](references/keypairs.md) <br>
- [ECS tags](references/tags.md) <br>
- [ECS monitoring and events](references/monitoring-events.md) <br>
- [Alibaba Cloud ECS API sources](references/sources.md) <br>
- [Official ECS API overview](https://www.alibabacloud.com/help/en/ecs/developer-reference/api-ecs-2014-05-26-overview) <br>
- [Official RunCommand API](https://www.alibabacloud.com/help/en/ecs/developer-reference/runcommand) <br>
- [Official DescribeInstances API](https://www.alibabacloud.com/help/en/ecs/developer-reference/describeinstances) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with Python SDK examples, shell commands, and JSON or TSV evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts write inventory, monitoring, and remote-command evidence under output/aliyun-ecs-manage/ when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
