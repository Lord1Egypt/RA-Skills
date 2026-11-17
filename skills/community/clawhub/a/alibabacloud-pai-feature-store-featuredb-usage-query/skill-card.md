## Description:

Queries FeatureDB read/write usage data from PAI-FeatureStore for consumption analysis, usage trends, and cost estimation with date range breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect historical PAI-FeatureStore FeatureDB read/write usage, review project or feature view trends, and estimate costs from query results.

### Deployment Geography for Use:

Supported Alibaba Cloud regions: cn-beijing, cn-hangzhou, cn-shanghai, cn-shenzhen, cn-hongkong, ap-southeast-1, ap-southeast-5, us-west-1, eu-central-1.

## Known Risks and Mitigations:

Risk: The documented install path includes remote shell execution with curl piped to bash.

Mitigation: Review installer contents first or use a package manager or manually verified Aliyun CLI binary instead.

Risk: Global automatic plugin installation and unscoped plugin updates can persistently change the local Aliyun CLI environment.

Mitigation: Enable automatic plugin installation and run plugin updates only in an approved, isolated CLI profile or environment.

Risk: FeatureDB usage outputs and CLI configuration checks may expose sensitive account or resource metadata.

Mitigation: Use a dedicated least-privilege Alibaba Cloud identity and avoid sharing credentials, shell history, logs, or raw command output unnecessarily.

## Reference(s):

- [Skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-pai-feature-store-featuredb-usage-query)
- [RAM Policies](references/ram-policies.md)
- [Related APIs and CLI Commands](references/related-apis.md)
- [Verification Method](references/verification-method.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [PAI-FeatureStore API Overview](https://www.alibabacloud.com/help/pai-feature-store/latest/api-overview)
- [Aliyun CLI Plugin Mode Documentation](https://www.alibabacloud.com/help/cli/cli-v3-0)
- [RAM Best Practices](https://www.alibabacloud.com/help/ram/security-practices/security-best-practices)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tabular usage analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read/write counts, cost calculations, usage trend summaries, and next-step guidance.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
