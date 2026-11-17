## Description: <br>
Query and manage Alibaba Cloud RDS instances in a user's Alibaba Cloud account through Alibaba Cloud CLI and official RDS, VPC, BssOpenApi, and DAS OpenAPIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators, database administrators, and developers use this skill to inventory Alibaba Cloud RDS resources and perform explicitly approved RDS lifecycle operations through the Alibaba Cloud CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform powerful Alibaba Cloud RDS mutations that may create costs, expose access, restart services, or delete instances. <br>
Mitigation: Use a least-privilege RAM user or role, prefer read-only permissions unless mutations are needed, set the intended region explicitly, and review every mutation confirmation before approval. <br>
Risk: Billing and DAS queries can expose financial, SQL workload, and performance metadata. <br>
Mitigation: Grant billing and DAS permissions only to users authorized to view that data, and remove those permissions when the related capabilities are not needed. <br>
Risk: Credentials, STS tokens, signed requests, and database passwords could be exposed if command output is handled carelessly. <br>
Mitigation: Configure credentials through Alibaba Cloud CLI profiles, avoid storing secrets in files or environment variables, and redact sensitive dry-run output before displaying or retaining it. <br>


## Reference(s): <br>
- [Related APIs - RDS Instances Manage](references/related-apis.md) <br>
- [RAM Policies - RDS Instances Manage](references/ram-policies.md) <br>
- [Verification Method - RDS Instances Manage](references/verification-method.md) <br>
- [Acceptance Criteria - RDS Instances Manage](references/acceptance-criteria.md) <br>
- [Alibaba Cloud RDS OpenAPI 2014-08-15](https://help.aliyun.com/zh/rds/developer-reference/api-rds-2014-08-15-overview) <br>
- [Alibaba Cloud CLI RDS 2014-08-15](https://api.aliyun.com/api-tools/cli/Rds/2014-08-15) <br>
- [Alibaba Cloud DAS OpenAPI 2020-01-16](https://help.aliyun.com/zh/das/developer-reference/api-das-2020-01-16-overview) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash commands and concise operational summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Business API calls require Alibaba Cloud CLI readiness checks, scoped profile selection, per-task User-Agent tagging, and explicit confirmation before mutations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
