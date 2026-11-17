## Description:

Onboard Alibaba Cloud, AWS, or Tencent Cloud accounts and system roles into IDaaS EIAM, with verification, interrupted-setup recovery, and local input checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud identity administrators and developers use this skill to onboard or verify cloud accounts and system roles in IDaaS EIAM across Alibaba Cloud, AWS, and Tencent Cloud. It guides scoped discovery, confirmed configuration, health checks, and recovery from interrupted setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud configuration persists, and partial failures may leave completed resources.

Mitigation: Use scoped cloud profiles, review the exact confirmed accounts, trust relationships, and policy changes before applying, then read back the target state after failures or timeouts.

Risk: The optional private-API transport may be unavailable and requires deployment authorization.

Mitigation: Use that transport only when deployment authorization is in place; otherwise stop and report the limitation rather than bypassing the authorization boundary.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-idaas-cloud-identity-setup)
- [Publisher profile](https://clawhub.ai/user/sdk-team)
- [Getting started](artifact/references/getting-started.md)
- [Setup](artifact/references/setup.md)
- [Alibaba Cloud](artifact/references/alibaba-cloud.md)
- [AWS](artifact/references/aws.md)
- [Tencent Cloud](artifact/references/tencent-cloud.md)
- [RAM identity](artifact/references/ram-identity.md)
- [RAM policies](artifact/references/ram-policies.md)
- [EIAM auxiliary API](artifact/references/eiam-auxiliary-api.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance and command examples, with structured JSON plans and verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses confirmed target and account details; does not include secrets in reported results.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
