## Description:

Allocates Elastic IP Addresses (EIPs) and binds them to existing Alibaba Cloud resources, including ECS instances, ENIs, CLB, NAT Gateway, HAVIP, and direct IP address bindings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and cloud operators use this skill to guide Aliyun CLI workflows for allocating or selecting an EIP, associating it with an existing Alibaba Cloud resource, verifying the binding, and handling cleanup after failed binds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup guidance may encourage piping a remote install script to a shell.

Mitigation: Use a verified package-manager install or pinned signed Aliyun CLI release before running the skill workflow.

Risk: Automatic Aliyun CLI plugin installation can make persistent environment changes.

Mitigation: Enable plugin auto-install only in an approved environment and review installed plugin versions before use.

Risk: Broad RAM credentials could allow higher-impact cloud operations than needed for EIP association.

Mitigation: Use tightly scoped RAM credentials limited to required EIP, validation, and cleanup actions for the target resources.

Risk: Linked acceptance and related API references include cloud creation and deletion operations outside the main EIP bind workflow.

Mitigation: Restrict production use to EIP-only operations and require explicit user confirmation before any release or deletion command.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-network-eip-associate)
- [ClawHub publisher profile](https://clawhub.ai/user/sdk-team)
- [EIP CLI Command Reference](references/cli-commands.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [EIP Associate RAM Permission Policies](references/ram-policies.md)
- [EIP Batch Associate Cloud Resources - Related APIs and CLI Commands](references/related-apis.md)
- [EIP Batch Associate Cloud Resources - Success Verification Method](references/verification-method.md)
- [Acceptance Criteria: alibabacloud-network-eip-associate](references/acceptance-criteria.md)
- [AssociateEipAddress API documentation](https://api.aliyun.com/document/Vpc/2016-04-28/AssociateEipAddress)
- [Aliyun CLI official documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Aliyun CLI command sequences and checks; execution requires user-provided Alibaba Cloud resource IDs, region, credentials, and confirmation for allocation or cleanup actions.]

## Skill Version(s):

0.0.1-beta.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
