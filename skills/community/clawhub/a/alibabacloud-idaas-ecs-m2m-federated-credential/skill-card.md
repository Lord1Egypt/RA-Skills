## Description:

Configures Alibaba Cloud IDaaS federation for ECS machine identities without AccessKeys, including M2M clients, federated credentials, and scoped inventory access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud administrators use this skill to configure Alibaba Cloud IDaaS/EIAM machine-to-machine federation for ECS identities without AccessKeys. It also guides scoped, read-only IDaaS and ECS inventory queries and token-exchange troubleshooting.

### Deployment Geography for Use:

Alibaba Cloud EIAM regions: cn-hangzhou, cn-beijing, cn-hongkong, ap-southeast-1, ap-southeast-5, ap-northeast-2, and eu-central-1.

## Known Risks and Mitigations:

Risk: Credential handling or cloud-resource selection could expose credentials or affect protected cloud resources; the security review is incomplete.

Mitigation: Keep credentials in the configured local CLI environment, verify the account, region, and target resource IDs, and review the security findings before running setup or token-exchange steps.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-idaas-ecs-m2m-federated-credential)
- [OpenAPI contracts](artifact/references/openapi-contracts.md)
- [API and pitfalls](artifact/references/api-and-pitfalls.md)
- [RAM policies](artifact/references/ram-policies.md)
- [CLI installation guide](artifact/assets/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with setup guidance, shell commands, configuration details, and API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tables, error diagnostics, and redacted token summaries.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
