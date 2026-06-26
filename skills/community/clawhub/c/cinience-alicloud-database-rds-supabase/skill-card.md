## Description: <br>
Manage Alibaba Cloud RDS Supabase instances and related RDS AI Service configuration through OpenAPI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to create, query, start, stop, restart, and configure Alibaba Cloud RDS Supabase application instances. It is suited for RDS AI Service administration tasks involving authentication, storage, RAG, SSL, IP allowlists, endpoints, and instance details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact database administration actions, including delete, stop, restart, password, authentication, SSL, and IP whitelist changes. <br>
Mitigation: Use a dedicated least-privilege Alibaba Cloud RAM credential and require explicit confirmation before any destructive or security-sensitive change. <br>
Risk: Saved API responses may contain sensitive database, endpoint, authentication, storage, or configuration details. <br>
Mitigation: Review and redact saved outputs before sharing or retaining them outside the operational context. <br>
Risk: Running actions against an unintended region or instance can affect the wrong RDS Supabase resource. <br>
Mitigation: Specify the exact RegionId and instance ID, and ask the user to confirm them when they are missing or ambiguous. <br>


## Reference(s): <br>
- [API overview](references/api_overview.md) <br>
- [Core API parameter reference](references/api_reference.md) <br>
- [Cross-region query examples](references/query-examples.md) <br>
- [Official documentation source list](references/sources.md) <br>
- [Alibaba Cloud RDS AI API overview](https://api.aliyun.com/document/RdsAi/2025-05-07/overview) <br>
- [Alibaba Cloud RDS Supabase documentation](https://www.alibabacloud.com/help/zh/rds/apsaradb-rds-for-postgresql/supabase/) <br>
- [Alibaba Cloud RDS AI API directory](https://www.alibabacloud.com/help/zh/rds/apsaradb-rds-for-postgresql/api-rdsai-2025-05-07-dir-postgresql/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with API operation names, parameters, and optional shell or SDK command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write saved results or API responses under output/database-rds-supabase/ when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
