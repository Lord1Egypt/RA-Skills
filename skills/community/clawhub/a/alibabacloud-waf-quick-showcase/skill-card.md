## Description:

Solution skill for using Alibaba Cloud WAF to protect web applications on ECS by deploying VPC networking, security groups, ECS instances, a sample application, and WAF integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to run a guided Alibaba Cloud WAF protection experience that provisions new VPC and ECS infrastructure, configures a sample web application, and integrates it with a new or existing WAF instance.

### Deployment Geography for Use:

Global where Alibaba Cloud WAF, ECS, and VPC services are available.

## Known Risks and Mitigations:

Risk: Mutable CLI installation and plugin updates can change local CLI behavior before execution.

Mitigation: Review before installing, avoid curl | bash and unverified latest binaries, and only enable automatic plugin installation when accepting that local CLI behavior may change.

Risk: The workflow creates billable Alibaba Cloud resources and opens ECS HTTP access to the internet.

Mitigation: Use a test account with narrow RAM permissions, confirm expected costs before creation, and restrict or remove the public ECS security-group rule after testing.

Risk: The workflow may involve reusable passwords or cloud credentials during operation.

Mitigation: Prefer SSH keys or temporary credentials where possible and redact passwords from commands, logs, and user-facing error output.

## Reference(s):

- [CLI Installation Guide](references/cli-installation-guide.md)
- [RAM Permissions Required](references/ram-policies.md)
- [Related APIs](references/related-apis.md)
- [Success Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Alibaba Cloud WAF protection solution](https://www.aliyun.com/solution/tech-solution/web-protection/2714251)
- [VPC API reference](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-createvpc)
- [ECS API reference](https://help.aliyun.com/zh/ecs/developer-reference/api-ecs-2014-05-26-overview)
- [WAF 3.0 API reference](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/developer-reference/api-waf-openapi-2021-10-01-overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and parameter prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require user-confirmed Alibaba Cloud parameters; displayed passwords should be redacted.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
