## Description: <br>
Alibaba Cloud KMS Secret Management Skill for managing KMS secrets, including create, delete, update, query, version management, and rotation policy configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to generate and review Aliyun CLI and Python SDK workflows for Alibaba Cloud KMS secret lifecycle management, including secret creation, retrieval, rotation, restore, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Alibaba Cloud KMS permissions can affect production secrets and keys. <br>
Mitigation: Use a dedicated least-privilege RAM role scoped to required secrets and avoid wildcard policies. <br>
Risk: Secret retrieval and SDK examples can expose plaintext credentials in chat, terminal output, or shell history. <br>
Mitigation: Mask secret values by default, require explicit user confirmation before retrieval, and run retrieval only in a private environment with logging disabled. <br>
Risk: Secret deletion, rotation, and managed credential workflows can disrupt production systems. <br>
Mitigation: Verify the active account, region, and target secret before execution; prefer recoverable deletion and use change control for rotation of managed RDS, RAM, ECS, Redis, or PolarDB credentials. <br>


## Reference(s): <br>
- [Acceptance Criteria: KMS Secret Management Skill](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Managed Credentials Guide](references/managed-credentials.md) <br>
- [KMS Secret Management RAM Permission Policies](references/ram-policies.md) <br>
- [KMS Secret Management Related API List](references/related-apis.md) <br>
- [KMS Secret Management Verification Methods](references/verification-method.md) <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-kms-secret-manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Aliyun CLI commands and Python SDK examples; secret values should be masked unless explicitly requested and confirmed.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
