## Description: <br>
Use when managing Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07) via OpenAPI, including creating, starting/stopping/restarting instances, resetting passwords, querying endpoints/auth/storage, configuring auth/RAG/SSL/IP whitelist, and listing instance details or conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to administer Alibaba Cloud RDS Supabase resources through documented OpenAPI workflows, including instance lifecycle management, configuration, security settings, and verification queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide powerful cloud administration actions such as delete, stop, restart, password reset, IP whitelist, SSL, and auth changes. <br>
Mitigation: Require explicit approval for mutating operations, verify the target region and instance ID, and use least-privilege Alibaba Cloud RAM credentials. <br>
Risk: Incorrect region selection or instance identifiers could affect unintended Alibaba Cloud resources. <br>
Mitigation: Ask for clarification when the region or instance ID is unclear and run a minimal read-only query before executing the target operation. <br>


## Reference(s): <br>
- [API Overview](references/api_overview.md) <br>
- [Core API Parameter Quick Reference](references/api_reference.md) <br>
- [All-Region Query Examples](references/query-examples.md) <br>
- [Official Source List](references/sources.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/aliyun-rds-supabase) <br>
- [Alibaba Cloud RDS AI API Overview](https://api.aliyun.com/document/RdsAi/2025-05-07/overview) <br>
- [Alibaba Cloud RDS Supabase Documentation](https://www.alibabacloud.com/help/zh/rds/apsaradb-rds-for-postgresql/supabase/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with command examples, API parameter summaries, and evidence file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save command outputs, API response summaries, and reproducibility evidence under output/aliyun-rds-supabase/.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
