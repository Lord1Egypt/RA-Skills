## Description:

MaxCompute Quota Management Skill for managing MaxCompute/ODPS quota resources, including pay-as-you-go quota creation, query, and listing operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to list, query, and create Alibaba Cloud MaxCompute pay-as-you-go quota resources through guided Aliyun CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe setup instructions or unverified CLI installation paths could increase installation risk.

Mitigation: Prefer a verified Aliyun CLI installation path before installing or updating the MaxCompute plugin.

Risk: Quota management commands may expand permissions or create paid cloud resources.

Mitigation: Use a least-privilege RAM identity scoped to MaxCompute quotas and confirm all user-customizable parameters before execution.

Risk: Subscription quota examples may conflict with the intended pay-as-you-go workflow and could incur charges.

Mitigation: Do not run subscription quota creation examples; keep creation limited to pay-as-you-go quotas unless separately reviewed.

Risk: Generated result and log files may contain sensitive operational records.

Mitigation: Treat result and log files as sensitive records and protect or remove them according to local retention policy.

## Reference(s):

- [Related APIs](artifact/references/related-apis.md)
- [RAM Policies](artifact/references/ram-policies.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [MaxCompute Product](https://api.aliyun.com/product/MaxCompute)
- [CreateQuota API](https://api.aliyun.com/api/MaxCompute/2022-01-04/CreateQuota)
- [ListQuotas API](https://api.aliyun.com/api/MaxCompute/2022-01-04/ListQuotas)
- [Java SDK Documentation](https://help.aliyun.com/zh/sdk/developer-reference/v2-java-sdk)
- [Credential Management](https://help.aliyun.com/zh/sdk/developer-reference/v2-manage-access-credentials)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce quota result summaries and local operational logs when the skill workflow is executed.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
