## Description: <br>
Solution skill for using WAF to protect web applications on ECS by deploying network resources, ECS instances, and WAF integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to guide Aliyun CLI setup, create a new ECS-based web environment, and integrate Alibaba Cloud WAF protection. It supports a quick end-to-end WAF experience or integration with an existing WAF instance while creating new ECS and network resources. <br>

### Deployment Geography for Use: <br>
Global, subject to Alibaba Cloud WAF and ECS regional availability and account eligibility. <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create billable Alibaba Cloud resources such as ECS, WAF, VPC, security groups, and related networking components. <br>
Mitigation: Use a dedicated test account or least-privilege RAM role, confirm every region, resource, and password before execution, and plan cleanup after the showcase. <br>
Risk: The workflow depends on local Aliyun CLI installation, plugin updates, and authenticated CLI access. <br>
Mitigation: Prefer Homebrew or inspected manual CLI installation over curl-to-bash, verify Aliyun CLI version 3.3.3 or later, update plugins explicitly, and use OAuth or least-privilege temporary credentials. <br>
Risk: The workflow handles sensitive account context and an ECS login password during resource creation. <br>
Mitigation: Do not use AK/SK credentials, require user confirmation before resource creation, and redact passwords from displayed commands, logs, and error messages. <br>


## Reference(s): <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [RAM Permissions Required](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Success Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud WAF Web Protection Solution](https://www.aliyun.com/solution/tech-solution/web-protection/2714251) <br>
- [VPC API Reference](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-createvpc) <br>
- [ECS API Reference](https://help.aliyun.com/zh/ecs/developer-reference/api-ecs-2014-05-26-overview) <br>
- [WAF 3.0 API Reference](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/developer-reference/api-waf-openapi-2021-10-01-overview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI command sequences] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes user confirmations, Aliyun CLI OAuth setup, password redaction, and cleanup reminders for billable cloud resources.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
