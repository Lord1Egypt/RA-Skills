## Description: <br>
Manage Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07) via OpenAPI for instance lifecycle, passwords, endpoints, auth, storage, RAG, SSL, IP whitelist, instance details, and conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and cloud administrators use this skill to manage Alibaba Cloud RDS Supabase resources through OpenAPI workflows. It helps plan and execute lifecycle, configuration, security, auth, storage, RAG, and query operations with explicit region and instance scoping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide operations that make real changes to Alibaba Cloud RDS Supabase resources. <br>
Mitigation: Use least-privilege RAM credentials, require explicit approval for mutating operations, and verify the exact region and instance before execution. <br>
Risk: Saved outputs or API summaries may expose passwords, access keys, certificates, endpoints, or storage credentials. <br>
Mitigation: Redact sensitive values before saving or sharing outputs, and store only the minimum evidence needed for reproducibility. <br>
Risk: Broad all-region queries can expand operational scope beyond the user's intended target. <br>
Mitigation: Prefer an explicit region, ask when the region is unclear, and use all-region queries only when necessary or user-approved. <br>


## Reference(s): <br>
- [API overview and operation groups](references/api_overview.md) <br>
- [Core API parameter quick reference](references/api_reference.md) <br>
- [All-region query examples](references/query-examples.md) <br>
- [Official source list](references/sources.md) <br>
- [Alibaba Cloud RDS AI Service API overview](https://api.aliyun.com/document/RdsAi/2025-05-07/overview) <br>
- [Alibaba Cloud RDS Supabase documentation](https://www.alibabacloud.com/help/zh/rds/apsaradb-rds-for-postgresql/supabase/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline command examples, parameter guidance, and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save sanitized artifacts, command outputs, and API response summaries under output/alicloud-database-rds-supabase/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
