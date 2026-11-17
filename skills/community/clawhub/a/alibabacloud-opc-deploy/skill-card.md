## Description:

Guides Chinese-speaking users through choosing an Alibaba Cloud OPC package and provisioning its cloud resources with the Aliyun CLI after explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and small business builders use this skill to settle an OPC SKU, prepare Alibaba Cloud credentials, review costs, and create or verify the package resources step by step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create paid Alibaba Cloud resources after confirmation.

Mitigation: Review the resource list, itemized pricing, and payment confirmation before allowing any paid operation.

Risk: The skill can install or update local Alibaba Cloud CLI tooling and enable CLI plugin auto-install.

Mitigation: Review the CLI setup steps before installation and confirm that changes to the local AI tool and Aliyun CLI environment are acceptable.

Risk: Credential setup and live cloud resources can affect the user's Alibaba Cloud account.

Mitigation: Use the documented dedicated RAM role and least-privilege policy, and do not share AccessKey or SecretKey values in chat.

Risk: Provisioned web resources may expose public HTTP and HTTPS ports.

Mitigation: Confirm public exposure during payment authorization and keep SSH restricted to the user's current IP address.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-opc-deploy)
- [Execution Phases](references/execution-phases.md)
- [Aliyun CLI Capability Matrix](references/cli_capability_matrix.md)
- [Credential Setup](references/credential-setup.md)
- [RAM Policy](references/ram-policies.md)
- [SKU Resolution](references/sku-resolution.md)
- [SKU Parameter Format](references/sku-params-format.md)
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/)
- [SWAS API Overview](https://help.aliyun.com/zh/simple-application-server/developer-reference/api-swas-open-2020-06-01-overview)
- [ECS RunInstances API](https://help.aliyun.com/zh/ecs/developer-reference/api-ecs-2014-05-26-runinstances)
- [ESA PurchaseRatePlan API](https://help.aliyun.com/zh/edge-security-acceleration/esa/api-esa-2024-09-10-purchaserateplan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Chinese Markdown guidance with inline shell commands, configuration snippets, and local deployment records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing output is zh-CN; paid Alibaba Cloud operations require explicit confirmation before execution.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
