## Description: <br>
Alibaba Cloud MongoDB full lifecycle management for creating, querying, scaling, securing, backing up, upgrading, and deleting standalone, replica set, and sharded cluster instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to administer Alibaba Cloud ApsaraDB for MongoDB instances through guided Aliyun CLI workflows. It supports lifecycle operations including provisioning, querying, scaling, security configuration, backup, upgrade, billing conversion, renewal, node management, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad, costly, or destructive Alibaba Cloud changes. <br>
Mitigation: Install only for agents expected to administer ApsaraDB for MongoDB, and use a dedicated least-privilege RAM user or role scoped to required regions and resources. <br>
Risk: Billing, purchase, renewal, public-network, KMS, password reset, and deletion operations can materially affect cost, access, or data availability. <br>
Mitigation: Require manual approval before these operations and avoid granting BSS, KMS, resource-group, public-network, billing, or delete permissions unless the task requires them. <br>
Risk: The skill requires sensitive cloud credentials. <br>
Mitigation: Prefer short-lived credentials and avoid placing real secrets in command arguments, shell profiles, logs, or user-visible output. <br>


## Reference(s): <br>
- [Operations](artifact/references/operations.md) <br>
- [Related APIs](artifact/references/related-apis.md) <br>
- [RAM Policies](artifact/references/ram-policies.md) <br>
- [Verification Method](artifact/references/verification-method.md) <br>
- [CLI Installation Guide](artifact/references/cli-installation-guide.md) <br>
- [Acceptance Criteria](artifact/references/acceptance-criteria.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-mongodb-instances-manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, parameter summaries, and operation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on actual Alibaba Cloud API or CLI results when reporting resource state.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
