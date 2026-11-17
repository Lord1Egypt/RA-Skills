## Description:

Alibaba Cloud AnalyticDB for MySQL Operations & Diagnosis Assistant that supports cluster information queries, performance monitoring, slow query diagnosis, running SQL analysis, and table-level optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Alibaba Cloud operators use this skill to inspect ADB MySQL clusters, review performance and storage status, and request slow-query or table-modeling diagnostics through Alibaba Cloud CLI/API workflows.

### Deployment Geography for Use:

Global, where the referenced Alibaba Cloud ADB MySQL regions are available.

## Known Risks and Mitigations:

Risk: Setup instructions include unverified install or update paths for Aliyun CLI components.

Mitigation: Use a trusted package manager or a pinned, verified Aliyun CLI release, and avoid automatic plugin installation or unpinned plugin updates.

Risk: The skill requires authenticated Alibaba Cloud access and may interact with persistent cloud credentials.

Mitigation: Use least-privilege read-only RAM permissions, prefer temporary or role-based credentials, and do not paste cloud secrets into commands or agent conversations.

Risk: Diagnostic requests can send cluster IDs, region information, and diagnostic questions to Alibaba Cloud endpoints.

Mitigation: Confirm the target region and cluster before execution, review generated commands, and avoid including unnecessary sensitive business details in diagnostic questions.

## Reference(s):

- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [Cluster Intelligent Diagnosis](references/cluster-diagnosis.md)
- [Cluster Information Query](references/cluster-info.md)
- [RAM Policy - ADB MySQL Operations and Diagnosis Assistant](references/ram-policies.md)
- [Alibaba Cloud Region ID List](references/region-list.md)
- [Verification Methods](references/verification-method.md)
- [Alibaba Cloud CLI credential configuration documentation](https://help.aliyun.com/zh/cli/configure-credentials)
- [Aliyun CLI plugin repository](https://github.com/aliyun/aliyun-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with command strings, CLI snippets, diagnostic summaries, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Aliyun CLI profile and ADB MySQL region or cluster context for instance-level diagnostics.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
