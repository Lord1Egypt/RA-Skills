## Description: <br>
Alibaba Cloud Security Center (SAS) agent onboarding and management assistant for installing, managing, troubleshooting, and scanning security agents with the aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and security engineers use this skill to onboard servers to Alibaba Cloud Security Center, manage agent authorization and lifecycle tasks, and run supported security checks against Alibaba Cloud assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run privileged agent installs, Cloud Assistant commands, authorization changes, paid feature changes, uninstalls, and security scan dispatches in live Alibaba Cloud environments. <br>
Mitigation: Require explicit user confirmation before every write operation, show the exact command or change before execution, and use least-privilege RAM credentials or temporary roles. <br>
Risk: The skill requires sensitive Alibaba Cloud credentials and may interact with paid Security Center features. <br>
Mitigation: Use only accounts and servers the operator controls, never expose AccessKey or SecretKey values, and confirm billing-impacting actions before enabling or changing paid features. <br>
Risk: Installer and persistent-agent behavior can affect servers beyond the current session. <br>
Mitigation: Prefer verified package installation over curl-to-bash where possible, verify installer sources, monitor local CLI configuration changes, and confirm agent status after installation or removal. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Security Center Agent Install Guide](references/agent-install-guide.md) <br>
- [API Reference](references/api-reference.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Install Scenarios](references/install-scenarios.md) <br>
- [Manage Scenarios](references/manage-scenarios.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Aliyun CLI Setup Script](https://aliyuncli.alicdn.com/setup.sh) <br>
- [Alibaba Cloud Security Center Billing Overview](https://help.aliyun.com/zh/security-center/product-overview/billing-overview) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and CLI/API parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Alibaba Cloud credentials, aliyun CLI access, explicit confirmation for write operations, and least-privilege RAM permissions.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
