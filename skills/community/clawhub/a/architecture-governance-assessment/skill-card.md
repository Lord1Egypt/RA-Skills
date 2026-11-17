## Description:

Architecture governance and assessment tool. Evaluate cloud architectures against best practices and generate actionable improvement reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2513483494](https://clawhub.ai/user/2513483494)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to query Tencent Cloud Smart Advisor architecture data, review assessment results, and prepare actionable governance guidance for cloud architectures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud credentials and may guide users toward durable AK/SK configuration.

Mitigation: Use a tightly scoped sub-account or short-lived credentials and avoid storing long-lived AK/SK values in shell startup files.

Risk: IAM role creation, policy attachment, Smart Advisor authorization, and cloud cleanup can change cloud account state.

Mitigation: Review the requested CAM role, attached policies, authorization request, and cleanup target before approving any write operation.

Risk: Generated console login links can grant access during their validity window.

Mitigation: Do not share generated login links and regenerate them only for the intended user and target console page.

Risk: The security verdict is suspicious due to credential, IAM, console-login, cleanup, and network behavior.

Mitigation: Scan and review the skill before deployment, then run it only in accounts where the requested Tencent Cloud access is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2513483494/skills/architecture-governance-assessment)
- [Tencent Cloud official site](https://cloud.tencent.com)
- [Tencent Cloud API endpoint pattern](https://*.tencentcloudapi.com)
- [CreateAdvisorAuthorization API reference](artifact/references/api/CreateAdvisorAuthorization.md)
- [DescribeArch API reference](artifact/references/api/DescribeArch.md)
- [DescribeArchList API reference](artifact/references/api/DescribeArchList.md)
- [DescribeLastEvaluation API reference](artifact/references/api/DescribeLastEvaluation.md)
- [DescribeStrategies API reference](artifact/references/api/DescribeStrategies.md)
- [ListDirectoryV2 API reference](artifact/references/api/ListDirectoryV2.md)
- [ListUnorganizedDirectory API reference](artifact/references/api/ListUnorganizedDirectory.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated Tencent Cloud console login links and account-scoped Smart Advisor assessment data.]

## Skill Version(s):

1.4.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
