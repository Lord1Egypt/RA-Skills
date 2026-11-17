## Description:

Cloud Architecture Canvas helps agents use Tencent Cloud Smart Advisor APIs to inspect cloud architecture directories, architecture details, Well-Architected evaluation results, risk assessment items, service authorization, and console access links for the current Tencent Cloud account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2513483494](https://clawhub.ai/user/2513483494)

### License/Terms of Use:

MIT-0

## Use Case:

External users, cloud engineers, and developers use this skill to query Tencent Cloud Smart Advisor architecture data, review risk and evaluation results, and generate guided Tencent Cloud console access for the currently configured account. It is intended for account-scoped cloud architecture review workflows that require Tencent Cloud API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Tencent Cloud API credentials and can create or use console-login CAM roles.

Mitigation: Use a dedicated least-privilege subaccount or temporary credentials, avoid storing long-term AK/SK values in shell profiles, review role policies before creation, and require explicit consent before role creation or service authorization.

Risk: The security review notes unsafe transport and scoping gaps, including TLS fallback and host allowlisting concerns.

Mitigation: Do not use the skill in environments where certifi may be missing until those issues are fixed, and restrict network access to the required Tencent Cloud endpoints.

## Reference(s):

- [Cloud Architecture Canvas on ClawHub](https://clawhub.ai/2513483494/skills/cloud-architecture-canvas)
- [Tencent Cloud Smart Advisor documentation](https://cloud.tencent.com/document/product/1278/109059)
- [Tencent Cloud](https://cloud.tencent.com)
- [CreateAdvisorAuthorization API reference](references/api/CreateAdvisorAuthorization.md)
- [DescribeArch API reference](references/api/DescribeArch.md)
- [DescribeArchList API reference](references/api/DescribeArchList.md)
- [DescribeLastEvaluation API reference](references/api/DescribeLastEvaluation.md)
- [DescribeStrategies API reference](references/api/DescribeStrategies.md)
- [ListDirectoryV2 API reference](references/api/ListDirectoryV2.md)
- [ListUnorganizedDirectory API reference](references/api/ListUnorganizedDirectory.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON command outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account-scoped Tencent Cloud Smart Advisor results and console login links; long login URLs should be presented as Markdown links.]

## Skill Version(s):

1.4.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
