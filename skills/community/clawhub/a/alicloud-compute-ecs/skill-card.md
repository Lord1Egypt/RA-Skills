## Description: <br>
Manage Alibaba Cloud Elastic Compute Service (ECS) via OpenAPI/SDK for listing or creating instances, starting, stopping, and rebooting instances, managing disks, snapshots, images, security groups, key pairs, and network interfaces, querying status, and troubleshooting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to administer Alibaba Cloud ECS resources through OpenAPI, SDK examples, and inventory or troubleshooting scripts. It helps agents plan and execute ECS workflows while preserving region, resource identifier, and output evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions against live Alibaba Cloud ECS infrastructure. <br>
Mitigation: Use least-privilege RAM credentials and confirm the region, resource IDs, and intended effect before mutating resources. <br>
Risk: Remote commands, deletion, disk reset or replacement, snapshot or image deletion, and security group changes can disrupt workloads or expose systems. <br>
Mitigation: Require explicit approval for these operations and review generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-compute-ecs) <br>
- [ECS API overview](https://www.alibabacloud.com/help/en/ecs/developer-reference/api-ecs-2014-05-26-overview) <br>
- [DescribeInstances API](https://www.alibabacloud.com/help/en/ecs/developer-reference/describeinstances) <br>
- [RunCommand API](https://www.alibabacloud.com/help/en/ecs/developer-reference/runcommand) <br>
- [ECS endpoints](https://www.alibabacloud.com/help/en/ecs/developer-reference/endpoints) <br>
- [Skill source references](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples, plus JSON or TSV files from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts write operational evidence under output/alicloud-compute-ecs/ when requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
