## Description:

Architecture dashboard with integrated risk review. Monitor architecture health, track risk items, and get Well-Architected scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stinggit](https://clawhub.ai/user/stinggit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud architects use this skill to inspect Tencent Cloud Smart Advisor architecture diagrams, retrieve Well-Architected evaluation results, review risk items, and generate console navigation guidance for the current Tencent Cloud account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for powerful Tencent Cloud access.

Mitigation: Use only narrowly scoped Tencent Cloud credentials and review the requested CAM and Advisor permissions before installation.

Risk: Long-lived AK/SK values may be written into shell startup files during setup.

Mitigation: Avoid persistent long-lived credentials where possible and prefer narrowly scoped or temporary credentials for sensitive environments.

Risk: Role creation, role cleanup, and Smart Advisor authorization can change cloud account state.

Mitigation: Run role creation, cleanup, or CreateAdvisorAuthorization only after explicit user approval and after confirming the CAM permissions and deletion behavior.

Risk: The generic API client and TLS fallback are not suitable for sensitive environments without review.

Mitigation: Fix the API client and TLS fallback before using the skill in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stinggit/skills/architecture-dashboard-risk-review)
- [Tencent Cloud Documentation](https://cloud.tencent.com)
- [Tencent Cloud Advisor Console](https://console.cloud.tencent.com/advisor)
- [CreateAdvisorAuthorization API Reference](artifact/references/api/CreateAdvisorAuthorization.md)
- [DescribeArch API Reference](artifact/references/api/DescribeArch.md)
- [DescribeArchList API Reference](artifact/references/api/DescribeArchList.md)
- [DescribeLastEvaluation API Reference](artifact/references/api/DescribeLastEvaluation.md)
- [DescribeStrategies API Reference](artifact/references/api/DescribeStrategies.md)
- [ListDirectoryV2 API Reference](artifact/references/api/ListDirectoryV2.md)
- [ListUnorganizedDirectory API Reference](artifact/references/api/ListUnorganizedDirectory.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate short-lived Tencent Cloud console links and account-scoped architecture or risk review summaries.]

## Skill Version(s):

1.4.0 (source: server evidence release.version and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
