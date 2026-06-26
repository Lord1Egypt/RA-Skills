## Description: <br>
Alibaba Cloud Milvus full-stack skill for control-plane instance management with aliyun CLI and data-plane Milvus operations with pymilvus, including instance setup, scaling, networking, collection management, vector search, hybrid search, indexing, partitions, databases, and RBAC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Alibaba Cloud Milvus instances and implement Milvus data-plane workflows with Python. It supports lifecycle, network, access-control, vector search, hybrid search, indexing, and retrieval-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help make real Alibaba Cloud Milvus resource, network, credential, and access-control changes. <br>
Mitigation: Install only for Milvus management use cases, use a tightly scoped RAM account, review every command before execution, and require explicit approval for create, scale, public network, ACL, service-role, and resource-group changes. <br>
Risk: Credentials, passwords, tokens, or private media could be exposed through prompts, commands, or examples. <br>
Mitigation: Do not paste real passwords or private media into examples, prefer scoped credentials, and avoid persisting secrets in generated code or shell history. <br>
Risk: Destructive data-plane or configuration operations can remove data or change availability. <br>
Mitigation: Require explicit confirmation before destructive operations such as collection drops, database drops, large deletes, config changes, or disabling public network access. <br>
Risk: Untrusted user input passed into shell commands or SDK code can produce unsafe or incorrect operations. <br>
Mitigation: Validate user-provided identifiers, regions, instance IDs, JSON bodies, and command parameters before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-milvus-manage) <br>
- [API Parameter Reference](references/api-reference.md) <br>
- [Collection Management](references/collection.md) <br>
- [CreateInstance Parameter Reference](references/create-params.md) <br>
- [Database Management](references/database.md) <br>
- [Quick Start: Create Your First Milvus Instance from Scratch](references/getting-started.md) <br>
- [Index Management](references/index.md) <br>
- [Instance Full Lifecycle](references/instance-lifecycle.md) <br>
- [Daily Operations](references/operations.md) <br>
- [Partition Management](references/partition.md) <br>
- [Common Patterns](references/patterns.md) <br>
- [RAM Permission Statement](references/ram-policies.md) <br>
- [User and Role Management](references/user-role.md) <br>
- [Vector Operations](references/vector.md) <br>
- [Alibaba Cloud Milvus Console](https://milvus.console.aliyun.com/#/overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud CLI commands, pymilvus code, compact resource summaries, and review prompts for operations that affect cloud resources, networking, credentials, or access control.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
