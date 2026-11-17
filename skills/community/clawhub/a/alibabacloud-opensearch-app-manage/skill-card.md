## Description:

Alibaba Cloud OpenSearch instance management skill for creating, listing, and describing OpenSearch instances, also referred to as app groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud OpenSearch app groups through Aliyun CLI workflows. It helps generate commands and guidance for creation, listing, description, permission checks, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may run mutable remote installers or latest archives.

Mitigation: Independently verify the installer source and integrity before running curl-to-bash or latest-archive installation steps.

Risk: Automatic plugin installation and plugin updates can change local Aliyun CLI state globally.

Mitigation: Review plugin changes before enabling auto installation or running global plugin updates, especially on shared or production workstations.

Risk: Create operations can provision billable Alibaba Cloud OpenSearch resources.

Mitigation: Use dry-run first, confirm all cost-related parameters with the user, and require least-privilege RAM permissions before executing create commands.

Risk: Cloud credentials could be exposed or over-privileged.

Mitigation: Use environment variables or preconfigured profiles, avoid printing secrets, and prefer RAM users or roles with only the required OpenSearch permissions.

## Reference(s):

- [Skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-opensearch-app-manage)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md)
- [RAM Policies](references/ram-policies.md)
- [Related APIs](references/related-apis.md)
- [Verification Method](references/verification-method.md)
- [Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/)
- [OpenSearch CreateAppGroup API](https://api.aliyun.com/document/OpenSearch/2017-12-25/CreateAppGroup)
- [OpenSearch ListAppGroups API](https://api.aliyun.com/document/OpenSearch/2017-12-25/ListAppGroups)
- [OpenSearch DescribeAppGroup API](https://api.aliyun.com/document/OpenSearch/2017-12-25/DescribeAppGroup)
- [Alibaba Cloud RAM Policy Overview](https://help.aliyun.com/document_detail/93732.html)
- [OpenSearch Authorization Rules](https://help.aliyun.com/zh/open-search/industry-algorithm-edition/authorization-rules-of-applications)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers Aliyun CLI setup, credential posture, RAM checks, parameter confirmation, dry-run, idempotency tokens, and OpenSearch create/list/describe workflows.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
