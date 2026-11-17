## Description:

Use when managing Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07) via OpenAPI, including creating, starting/stopping/restarting instances, resetting passwords, querying endpoints/auth/storage, configuring auth/RAG/SSL/IP whitelist, and listing instance details or conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud RDS Supabase app instances and related RDS AI Service configuration through OpenAPI workflows. It supports lifecycle, auth, storage, RAG, IP whitelist, SSL, endpoint, and conversation-related tasks with explicit region and credential handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may be over-scoped or exposed through prompts, logs, or saved outputs.

Mitigation: Use least-privilege RAM roles or short-lived credentials, prefer environment variables, and redact passwords and secrets from logs and saved artifacts.

Risk: Lifecycle and security operations can stop, delete, restart, or reconfigure live RDS Supabase resources.

Mitigation: Require explicit confirmation before destructive or security-sensitive operations, use bounded region and instance scope, and verify state after changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cinience/skills/aliyun-rds-supabase)
- [API overview and operation groups](references/api_overview.md)
- [Core API parameter quick reference](references/api_reference.md)
- [All-region query examples](references/query-examples.md)
- [Official source list](references/sources.md)
- [Alibaba Cloud RDS AI Service API overview](https://api.aliyun.com/document/RdsAi/2025-05-07/overview)
- [Alibaba Cloud RDS Supabase documentation](https://www.alibabacloud.com/help/zh/rds/apsaradb-rds-for-postgresql/supabase/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration guidance, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save artifacts, command outputs, and API response summaries under output/aliyun-rds-supabase/ when requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
