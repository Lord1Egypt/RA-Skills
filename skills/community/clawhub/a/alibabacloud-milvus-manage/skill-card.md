## Description:

Alibaba Cloud Milvus full-stack Skill for control-plane instance management with aliyun CLI and data-plane Milvus operations with pymilvus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Alibaba Cloud managed Milvus instances, configure networking and scaling, and operate Milvus collections, vectors, indexes, partitions, databases, and RBAC through pymilvus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact Alibaba Cloud and Milvus operations with real credentials or production instances.

Mitigation: Review before installation, use least-privilege RAM policies scoped to specific instances, and confirm destructive or major configuration changes before execution.

Risk: Public network access, broad CIDRs, or public-read OSS media can expose sensitive systems or data.

Mitigation: Prefer private networking, restrict CIDRs narrowly, and avoid public-read OSS objects for sensitive media.

Risk: Credential handling examples can lead users to paste real passwords or tokens into commands, notebooks, logs, or chat transcripts.

Mitigation: Use placeholders or secure secret handling, and do not paste real passwords into commands, notebooks, logs, or chat transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-milvus-manage)
- [Alibaba Cloud Milvus Console](https://milvus.console.aliyun.com/#/overview)
- [API Parameter Reference](references/api-reference.md)
- [Collection Management](references/collection.md)
- [CreateInstance Parameter Reference](references/create-params.md)
- [Database Management](references/database.md)
- [Quick Start](references/getting-started.md)
- [Index Management](references/index.md)
- [Instance Full Lifecycle](references/instance-lifecycle.md)
- [Daily Operations](references/operations.md)
- [Partition Management](references/partition.md)
- [Common Patterns](references/patterns.md)
- [RAM Permission Statement](references/ram-policies.md)
- [User and Role Management](references/user-role.md)
- [Vector Operations](references/vector.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include required Alibaba Cloud and PyMilvus User-Agent settings, ask for connection details before data-plane code, and request confirmation before destructive operations.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
