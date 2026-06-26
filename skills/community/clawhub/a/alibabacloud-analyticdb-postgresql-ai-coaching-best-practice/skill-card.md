## Description: <br>
Implement AI Coaching best practices on AnalyticDB for PostgreSQL (ADBPG) by using Supabase projects for training data management and ADBPG instances with vector optimization to build RAG-driven coaching systems for domain-specific workflows, decision-making, or skill development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to provision or configure Alibaba Cloud Supabase projects, ADBPG vector knowledge bases, and related network and database resources for RAG-powered coaching systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create billable Alibaba Cloud resources such as Supabase projects, ADBPG instances, NAT gateways, and EIPs. <br>
Mitigation: Require explicit user confirmation before any billable operation, review the proposed region and resource shape, and plan cleanup or release of resources after use. <br>
Risk: The workflow depends on cloud credentials, database passwords, namespace passwords, and API keys. <br>
Mitigation: Use a dedicated least-privilege RAM identity, avoid production secrets and long-lived AK/SK values in chat, and mask credentials in all outputs. <br>
Risk: The skill can change network and security posture through VPC, SNAT, EIP, and whitelist operations. <br>
Mitigation: Review each network-changing command before execution and prefer least-privilege RAM policies with only the documented required permissions. <br>
Risk: Knowledge-base document uploads may expose sensitive data to the configured cloud service. <br>
Mitigation: Upload only approved non-sensitive documents and review data classification requirements before ingestion. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [Aliyun CLI Parameter Guide](references/cli-parameter-guide.md) <br>
- [Database Schema](references/database-schema.md) <br>
- [Alibaba Cloud RAM Permissions](references/ram-policies.md) <br>
- [Related APIs and CLI Commands](references/related-apis.md) <br>
- [Verification Methods](references/verification-method.md) <br>
- [Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/) <br>
- [Aliyun CLI Plugin Repository](https://github.com/aliyun/aliyun-cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-analyticdb-postgresql-ai-coaching-best-practice) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational cloud setup guidance that requires user confirmation for billable resource creation and credential-sensitive steps.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
