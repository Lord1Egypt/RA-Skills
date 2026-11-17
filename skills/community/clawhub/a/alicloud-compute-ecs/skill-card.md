## Description:

Manage Alibaba Cloud Elastic Compute Service (ECS) via OpenAPI/SDK for instance inventory, lifecycle operations, storage, networking, monitoring, and troubleshooting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inventory and administer Alibaba Cloud ECS resources, including instances, disks, snapshots, images, security groups, key pairs, network interfaces, monitoring data, and Cloud Assistant remote commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide powerful ECS administration actions, including lifecycle changes, security group edits, disk and image operations, and Cloud Assistant remote commands.

Mitigation: Require human review before making changes, and use short-lived RAM credentials with least-privilege permissions.

Risk: Saved inventory and command-output JSON may expose account structure, instance identifiers, or command stdout.

Mitigation: Treat generated output files as sensitive and store or share them according to the user's cloud security policy.

Risk: Unreviewed SDK dependencies can affect the safety of cloud administration workflows.

Mitigation: Install dependencies in an isolated environment and prefer pinned, reviewed Alibaba Cloud SDK versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-compute-ecs)
- [ECS OpenAPI overview](https://www.alibabacloud.com/help/en/ecs/developer-reference/api-ecs-2014-05-26-overview)
- [ECS API metadata](https://api.aliyun.com/meta/v1/products/Ecs/versions/2014-05-26/api-docs.json)
- [ECS endpoints](https://www.alibabacloud.com/help/en/ecs/developer-reference/endpoints)
- [DescribeInstances API](https://www.alibabacloud.com/help/en/ecs/developer-reference/describeinstances)
- [RunCommand API](https://www.alibabacloud.com/help/en/ecs/developer-reference/runcommand)
- [Local API overview reference](references/api_overview.md)
- [Local source links reference](references/sources.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with inline shell commands, Python SDK examples, and JSON evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inventory and command outputs are saved under output/alicloud-compute-ecs/ when generated.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
