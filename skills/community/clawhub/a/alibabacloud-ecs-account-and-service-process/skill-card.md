## Description:

Handles Alibaba Cloud ECS account and process questions about account transfer, Simple Application Server boundaries, business contact routing, ticket progress triage, and instance tags and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud support agents and Alibaba Cloud customers use this skill to route ECS account and process questions, gather relevant account or instance evidence, and provide issue-specific guidance. Account-transfer changes require explicit customer confirmation, and commands run inside an instance require consent for that command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with high confidence because it reports capabilities beyond the stated support purpose, persistent CLI configuration changes, and cloud inventory or snapshot capabilities; the analysis is incomplete.

Mitigation: Review the flagged capabilities and CLI configuration effects, and resolve the incomplete analysis before installing; limit any inventory or snapshot operations to the customer's intended scope.

## Reference(s):

- [ECS account-transfer guide](https://help.aliyun.com/zh/ecs/user-guide/how-to-cross-account-transfer-migration-ecs-instance)
- [Simple Application Server overview](https://help.aliyun.com/zh/simple-application-server/product-overview/what-is-simple-application-server)
- [ECS image-copy guide](https://help.aliyun.com/zh/ecs/user-guide/copy-an-image)
- [ECS snapshot creation guide](https://help.aliyun.com/zh/ecs/user-guide/create-a-snapshot)
- [Account-transfer axis specification](artifact/references/axes/account-transfer-guide.md)
- [Instance-tag and metadata axis specification](artifact/references/axes/instance-tag-metadata-guide.md)
- [Issue-routing and contact guidance](artifact/references/axes/business-contact-routing.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, API calls]

**Output Format:** [Text and Markdown guidance, with command examples and structured API results where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests issue-specific identifiers as needed; gated changes require explicit confirmation and in-instance commands require per-command consent.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
