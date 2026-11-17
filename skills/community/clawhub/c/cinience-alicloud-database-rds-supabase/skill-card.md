## Description:

Manage Alibaba Cloud RDS Supabase through the RDS AI Service 2025-05-07 OpenAPI for instance lifecycle, password resets, endpoint and configuration queries, auth, RAG, SSL, IP whitelist, storage, and conversation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers and cloud operators use this skill to plan and execute Alibaba Cloud RDS Supabase management tasks through documented OpenAPI workflows. It is suited for creating, inspecting, starting, stopping, restarting, securing, and configuring RDS Supabase application instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers powerful cloud lifecycle and configuration actions, including deletes, stops, password resets, public endpoints, SSL, IP whitelist changes, and custom-agent changes.

Mitigation: Use a least-privilege RAM role and require human confirmation before any destructive, availability-impacting, credential-changing, or network-exposure-changing action.

Risk: Alibaba Cloud credentials and sensitive API responses may be exposed if copied into prompts, logs, or saved output.

Mitigation: Prefer environment variables or the standard Alibaba Cloud credentials file, avoid persisting raw credentials, and do not save sensitive API responses unless explicitly needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/cinience-alicloud-database-rds-supabase)
- [API Overview](references/api_overview.md)
- [Core API Reference](references/api_reference.md)
- [Region Query Examples](references/query-examples.md)
- [Official Documentation Sources](references/sources.md)
- [Alibaba Cloud RDS AI OpenAPI Overview](https://api.aliyun.com/document/RdsAi/2025-05-07/overview)
- [Alibaba Cloud RDS Supabase Documentation](https://www.alibabacloud.com/help/zh/rds/apsaradb-rds-for-postgresql/supabase/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with OpenAPI request guidance, configuration values, code snippets, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save requested results under output/database-rds-supabase/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
