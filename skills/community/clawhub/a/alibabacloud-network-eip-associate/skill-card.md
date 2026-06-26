## Description: <br>
Allocate Elastic IP Addresses (EIPs) and bind them to existing Alibaba Cloud resources across ECS instances, ENIs, CLB, NAT Gateway, HAVIP, and IP addresses, with allocation, binding, verification, and cleanup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud engineers and developers use this skill to allocate or select an Alibaba Cloud EIP, bind it to a user-specified existing resource, verify the association, and handle cleanup when binding fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through Alibaba Cloud networking operations that allocate, bind, unbind, or release EIPs and may incur cost or disrupt access. <br>
Mitigation: Use a dedicated least-privilege RAM user or short-lived credentials, isolate the Aliyun CLI profile, test in non-production where possible, and require manual confirmation before bind, unbind, release, create, or delete actions. <br>
Risk: Supporting references include broader VPC, ECS, NAT, and ALB create/delete commands beyond the core EIP association workflow. <br>
Mitigation: Treat broader create/delete references as review-only material unless deliberately operating in a disposable environment. <br>
Risk: Credential handling is required for Aliyun CLI access. <br>
Mitigation: Avoid root credentials, do not echo or expose access keys, prefer temporary credentials or role-based access, and scope permissions to the documented EIP operations. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/sdk-team/alibabacloud-network-eip-associate) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [EIP CLI Command Reference](references/cli-commands.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [EIP Associate RAM Permission Policies](references/ram-policies.md) <br>
- [Related APIs and CLI Commands](references/related-apis.md) <br>
- [Success Verification Method](references/verification-method.md) <br>
- [Alibaba Cloud AssociateEipAddress API](https://api.aliyun.com/document/Vpc/2016-04-28/AssociateEipAddress) <br>
- [Alibaba Cloud EIP Console](https://vpc.console.aliyun.com/eip) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and Alibaba Cloud CLI command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aliyun CLI 3.3.3 or later, an up-to-date CLI plugin set, an authenticated Alibaba Cloud profile, explicit user-provided region and resource IDs, and confirmation before allocation or cleanup actions.] <br>

## Skill Version(s): <br>
0.0.1-beta.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
