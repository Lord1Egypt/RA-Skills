## Description:

Helps agents use Tencent Cloud Smart Advisor APIs with AK/SK authentication to manage cloud architecture diagrams, retrieve evaluation results, query risk assessment items, and request service authorization with user consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2513483494](https://clawhub.ai/user/2513483494)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and cloud operations teams use this skill to inspect Tencent Cloud Smart Advisor architecture data, evaluation results, and risk checks for the current credentialed account. It also guides credential setup, role configuration, service authorization, and console access workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud credentials and may exercise broad IAM, STS, Advisor authorization, network, and login-link behaviors.

Mitigation: Install only after reviewing the requested permissions, use a dedicated least-privilege sub-account or short-lived credentials, and approve role creation or service authorization only when the action is expected.

Risk: Long-lived AK/SK credentials can be exposed if stored in persistent shell startup files or reused across accounts.

Mitigation: Prefer short-lived or dedicated credentials, avoid placing long-lived AK/SK values in shell startup files, and rotate credentials if they may have been exposed.

Risk: Generated Tencent Cloud console login links act as sensitive temporary access artifacts.

Mitigation: Treat generated login links as temporary credentials: do not share, cache, or log them, and regenerate links only for the intended session.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/2513483494/skills/arch-sla-cloudq)
- [Tencent Cloud Smart Advisor Documentation](https://cloud.tencent.com/document/product/1278/109059)
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi)
- [Tencent Cloud Smart Advisor Console](https://console.cloud.tencent.com/advisor)
- [README](artifact/README.md)
- [CreateAdvisorAuthorization API Reference](artifact/references/api/CreateAdvisorAuthorization.md)
- [DescribeArch API Reference](artifact/references/api/DescribeArch.md)
- [DescribeArchList API Reference](artifact/references/api/DescribeArchList.md)
- [DescribeLastEvaluation API Reference](artifact/references/api/DescribeLastEvaluation.md)
- [DescribeStrategies API Reference](artifact/references/api/DescribeStrategies.md)
- [ListDirectoryV2 API Reference](artifact/references/api/ListDirectoryV2.md)
- [ListUnorganizedDirectory API Reference](artifact/references/api/ListUnorganizedDirectory.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Tencent Cloud console login links and account-scoped Smart Advisor result summaries; credentials are not intended to be persisted by the skill.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
