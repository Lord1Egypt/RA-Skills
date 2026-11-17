## Description:

Deploys OpenClaw on an Alibaba Cloud ECS instance, configures Alibaba Cloud Bailian LLM access, and connects the deployment to a DingTalk bot for group chat use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to provision Alibaba Cloud ECS networking and compute resources, install OpenClaw, configure Bailian credentials, and verify DingTalk bot integration. It is intended for teams that want an AI assistant reachable from DingTalk group conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad Alibaba Cloud control to create compute, networking, security group, EIP, and model API key resources.

Mitigation: Use a dedicated temporary RAM role or isolated account and prefer the least-privilege policy documented in the artifact before running commands.

Risk: The deployment exposes services publicly and includes inbound SSH, HTTP, and HTTPS security group rules.

Mitigation: Restrict inbound rules, especially SSH, to trusted source IP ranges before testing or production use.

Risk: The workflow handles Bailian and DingTalk credentials and passes them into a remote installation process.

Mitigation: Avoid sharing secrets with unverified remote scripts, mask sensitive values in logs, and rotate Bailian and DingTalk credentials after testing.

Risk: Cloud resources and model usage can create ongoing cost and audit exposure.

Mitigation: Monitor billing and ActionTrail logs, and run the documented cleanup steps after testing when resources are no longer needed.

## Reference(s):

- [Bailian API Key Guide](references/bailian-api-key-guide.md)
- [DingTalk Bot Creation and Configuration Guide](references/dingtalk-setup-guide.md)
- [RAM Policies for OpenClaw ECS DingTalk Deployment](references/ram-policies.md)
- [Alibaba Cloud Deploy OpenClaw](https://help.aliyun.com/zh/simple-application-server/use-cases/quickly-deploy-and-use-openclaw)
- [DingTalk Open Platform ECS Deployment](https://open.dingtalk.com/document/dingstart/deployment-alibaba-cloud-ecs-server)
- [OpenClaw Official Website](https://openclaw.ai/)
- [Bailian Console](https://bailian.console.aliyun.com/)
- [DingTalk Open Platform](https://open.dingtalk.com/)
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-openclaw-ecs-dingtalk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment steps, validation checks, troubleshooting guidance, and cleanup instructions.]

## Skill Version(s):

0.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
