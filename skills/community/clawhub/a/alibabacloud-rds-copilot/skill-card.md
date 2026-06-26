## Description: <br>
Alibaba Cloud RDS Copilot intelligent operations assistant skill for RDS-related Q&A, SQL optimization, instance operations, and troubleshooting through Alibaba Cloud CLI and RdsAi OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database operators, and cloud engineers use this skill to query Alibaba Cloud RDS Copilot, diagnose RDS issues, optimize SQL, and interpret operational recommendations from RdsAi responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Alibaba Cloud credentials and may configure or use persistent local CLI profiles. <br>
Mitigation: Use a least-privilege RAM user or role, avoid root AccessKeys, rotate credentials, and configure credentials through Alibaba Cloud CLI rather than exposing secrets in chat or environment variables. <br>
Risk: RDS queries and troubleshooting prompts may send SQL literals, database identifiers, or production details to Alibaba Cloud RDS Copilot. <br>
Mitigation: Redact sensitive SQL values and production identifiers before sending queries, and avoid running examples in logged or shared environments unless the output is safe to expose. <br>
Risk: Recommendations from RDS Copilot may include SQL changes or operational steps that are unsafe to apply directly in production. <br>
Mitigation: Review generated recommendations, validate them in a test environment, and take backups or add restrictive conditions before executing high-impact SQL or operational changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-rds-copilot) <br>
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/) <br>
- [RDS AI Assistant Professional Edition Guide](https://help.aliyun.com/zh/rds/apsaradb-rds-for-mysql/manage-rds-colipot-professional-edition) <br>
- [Professional Edition activation page](https://rdsnext.console.aliyun.com/rdsCopilotProfessional/cn-hangzhou) <br>
- [Related APIs - RDS Copilot](references/related-apis.md) <br>
- [RAM Policies - RDS Copilot](references/ram-policies.md) <br>
- [Verification Method - RDS Copilot](references/verification-method.md) <br>
- [Acceptance Criteria - alibabacloud-rds-copilot](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with Alibaba Cloud CLI command blocks and natural-language analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include streaming JSON response interpretation, conversation IDs for follow-up calls, and credential setup guidance.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
