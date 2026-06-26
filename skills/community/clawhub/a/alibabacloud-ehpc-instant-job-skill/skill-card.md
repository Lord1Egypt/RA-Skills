## Description: <br>
Helps agents manage Alibaba Cloud E-HPC Instant jobs through Alibaba Cloud CLI or SDK workflows, including creating jobs, listing jobs, inspecting details and logs, and deleting jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to prepare Alibaba Cloud CLI or SDK access, validate E-HPC Instant job inputs, and manage job lifecycle operations for Alibaba Cloud compute workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through actions that create public, billable Alibaba Cloud resources or delete infrastructure. <br>
Mitigation: Use a dedicated least-privilege RAM user, review proposed create and delete operations, and require explicit user confirmation before changes. <br>
Risk: SDK examples may execute cloud mutations without the same interactive confirmation posture as guided CLI workflows. <br>
Mitigation: Avoid SDK examples unless a caller adds its own confirmation step and validates the target region, resource IDs, and costs. <br>
Risk: Long-running VM jobs may continue consuming resources after submission. <br>
Mitigation: Set appropriate job limits, monitor running jobs, inspect logs, and clean up completed or unwanted resources promptly. <br>


## Reference(s): <br>
- [E-HPC Instant CLI command reference](references/ehpcinstant.md) <br>
- [Alibaba Cloud CLI configuration guide](references/aliyun-cli.md) <br>
- [SDK credential configuration](references/CREDENTIALS.md) <br>
- [RAM permission policies](references/ram-policies.md) <br>
- [E-HPC Instant image management](references/instant-image.md) <br>
- [vSwitch management guide](references/vswitch.md) <br>
- [NAS storage management guide](references/storage.md) <br>
- [Compute resource configuration](references/resource.md) <br>
- [Job command configuration](references/job-command.md) <br>
- [Alibaba Cloud E-HPC Instant product documentation](https://help.aliyun.com/product/ehpcinstant.html) <br>
- [E-HPC Instant API documentation](https://api.aliyun.com/document/EhpcInstant/2023-07-01/overview) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/document_detail/121529.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and optional Python SDK examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud CLI commands and SDK examples that operate on cloud resources.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
