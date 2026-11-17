## Description:

Manage the lifecycle of Alibaba Cloud AnalyticDB for PostgreSQL Supabase projects, including listing, creation, pause and resume, password reset, API key retrieval, and security IP management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud ADBPG Supabase projects through Aliyun GPDB CLI workflows. It supports read-only inventory and credential queries as well as mutating lifecycle, password, and access-control operations with confirmation and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified Aliyun CLI installation, unpinned latest archives, and global plugin auto-update can introduce supply-chain risk.

Mitigation: Review installation steps before use; prefer pinned and verified packages or trusted package managers, and enable global plugin auto-update only when that operational risk is accepted.

Risk: The skill can retrieve or handle API keys, service-role keys, dashboard credentials, database passwords, and Alibaba Cloud access credentials.

Mitigation: Mask secrets in outputs, avoid logging full values, confirm sensitive operations, apply least-privilege RAM permissions, and rotate credentials after any exposure.

Risk: Create, pause, resume, password reset, and security IP changes can affect cost, availability, credentials, or network access.

Mitigation: Require explicit user confirmation for mutating operations, show key parameters before execution, and verify post-operation status with the documented GPDB checks.

## Reference(s):

- [CreateSupabaseProject parameters and defaults](references/create-supabase-project-parameters.md)
- [Related APIs for ADBPG Supabase management](references/related-apis.md)
- [RAM policies for ADBPG Supabase management](references/ram-policies.md)
- [Verification methods for ADBPG Supabase management](references/verification-method.md)
- [Acceptance criteria for ADBPG Supabase management](references/acceptance-criteria.md)
- [Aliyun CLI installation and configuration guide](references/cli-installation-guide.md)
- [Official CreateSupabaseProject API reference](https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/developer-reference/api-gpdb-2016-05-03-createsupabaseproject)
- [Official GPDB API documentation](https://help.aliyun.com/document_detail/86906.html)
- [Official Alibaba Cloud RAM access control documentation](https://help.aliyun.com/product/28625.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Aliyun CLI shell commands and JSON response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Aliyun CLI 3.3.3 or later, configured Alibaba Cloud credentials, confirmed user parameters, required RAM permissions, and the skill-specific user-agent.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
