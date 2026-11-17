## Description:

Manage Alibaba Cloud resources using the Aliyun CLI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hambaobao](https://clawhub.ai/user/hambaobao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to construct, explain, and review Aliyun CLI commands for Alibaba Cloud setup, authentication, and resource administration across ECS, VPC, OSS, RDS, SLB/CLB, RAM, DNS, and ACR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help produce high-impact cloud administration commands that change or delete Alibaba Cloud resources.

Mitigation: Verify regions and resource IDs before mutating commands, list targets before bulk deletion, and require explicit user confirmation for destructive operations.

Risk: Commands may expose or mishandle credentials when users pass passwords, access keys, or tokens directly in shells or transcripts.

Mitigation: Use least-privilege RAM users or roles, avoid root or AdministratorAccess unless explicitly required, and avoid putting real passwords or tokens directly in shell commands or shared transcripts.

Risk: Database, storage, DNS, and registry changes can be difficult or impossible to reverse.

Mitigation: Keep backups or rollback plans before changing or deleting databases, storage buckets or objects, DNS records, and container registry resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hambaobao/skills/aliyun-skills)
- [Aliyun CLI repository](https://github.com/aliyun/aliyun-cli)
- [Aliyun CLI setup reference](references/setup.md)
- [ECS reference](references/ecs.md)
- [VPC reference](references/vpc.md)
- [OSS reference](references/oss.md)
- [RDS reference](references/rds.md)
- [SLB / CLB reference](references/slb.md)
- [RAM reference](references/ram.md)
- [DNS reference](references/dns.md)
- [ACR reference](references/acr.md)
- [ossutil install and configure documentation](https://help.aliyun.com/zh/oss/developer-reference/install-and-configure-ossutil)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require configured Aliyun CLI credentials, explicit regions, resource IDs, and user confirmation before mutating operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
