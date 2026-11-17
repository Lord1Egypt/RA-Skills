## Description:

Manage Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07) via OpenAPI for instance lifecycle, password reset, endpoint/auth/storage queries, auth/RAG/SSL/IP whitelist configuration, and conversation listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to plan and execute Alibaba Cloud RDS Supabase administration tasks through OpenAPI. It helps scope regions and instance IDs, identify the relevant API operation, run bounded read or mutation workflows, and capture evidence for reproducibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact RDS Supabase administration actions, including delete, password reset, SSL, IP whitelist, auth, storage credential, and custom-agent changes.

Mitigation: Require explicit human confirmation for mutating operations and verify target region, instance ID, and operation scope before execution.

Risk: The skill relies on Alibaba Cloud credentials and may affect production database resources if granted broad permissions.

Mitigation: Use least-privilege RAM credentials, prefer environment variables or the standard credentials file, and start with a minimal read-only query to confirm permissions.

Risk: Ambiguous region selection can lead to queries or changes against the wrong resource scope.

Mitigation: Ask for the target region when unclear and run all-region queries only when explicitly needed or user-approved.

## Reference(s):

- [API overview and operation groups](references/api_overview.md)
- [Core API parameter quick reference](references/api_reference.md)
- [All-region query examples](references/query-examples.md)
- [Official source list](references/sources.md)
- [Alibaba Cloud RDS AI Service API overview](https://api.aliyun.com/document/RdsAi/2025-05-07/overview)
- [Alibaba Cloud RDS Supabase documentation](https://www.alibabacloud.com/help/zh/rds/apsaradb-rds-for-postgresql/supabase/)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-database-rds-supabase)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline commands, configuration notes, and API operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save command outputs, response summaries, and reproducibility evidence under output/alicloud-database-rds-supabase/.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
