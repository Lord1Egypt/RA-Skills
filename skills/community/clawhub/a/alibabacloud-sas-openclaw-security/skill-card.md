## Description:

Perform security operations on OpenClaw environments by calling Alibaba Cloud Security Center (SAS) and ECS APIs via the aliyun CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, cloud operators, and developers use this skill to inspect OpenClaw assets, review vulnerabilities, baseline findings, and alerts, trigger security checks, install guardrails, run approved Cloud Assistant commands, and generate operational security reports.

### Deployment Geography for Use:

Global; Alibaba Cloud Security Center and AI Security Center operations are documented for cn-shanghai and ap-southeast-1, while ECS Cloud Assistant operations must use the target instance region.

## Known Risks and Mitigations:

Risk: The skill can run remote commands on ECS hosts through Cloud Assistant.

Mitigation: Require human approval for the exact command and target instance list before execution, and restrict ecs:RunCommand permissions to specific ECS instances.

Risk: The skill can install mutable remote code on target ECS hosts.

Mitigation: Verify installer provenance out of band, review the generated install command before use, and run it only from a dedicated least-privileged Alibaba Cloud identity.

Risk: Broad cloud credentials could expand the impact of operational mistakes or misuse.

Mitigation: Use a dedicated RAM user or role with only the documented SAS, ECS, and AISC actions, and avoid primary account credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-sas-openclaw-security)
- [Security Operations Workflow](references/security_workflow.md)
- [Remediation, Hardening, and Product Recommendation Guide](references/remediation_guide.md)
- [RAM Permission Policy Reference](references/ram-policies.md)
- [Alibaba Cloud CLI Installation](https://help.aliyun.com/zh/cli/installation)
- [Security Center RAM Authentication](https://help.aliyun.com/zh/security-center/developer-reference/api-authentication-rules)
- [ECS RAM Authentication](https://help.aliyun.com/zh/ecs/developer-reference/authentication-rules-for-ecs-api)
- [RAM Custom Policies](https://help.aliyun.com/zh/ram/user-guide/create-a-custom-policy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON reports, terminal text, shell command proposals, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include raw Alibaba Cloud API responses, operational findings, remediation recommendations, and command execution results.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
