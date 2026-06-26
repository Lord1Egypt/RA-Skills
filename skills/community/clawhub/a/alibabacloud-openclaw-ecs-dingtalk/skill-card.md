## Description: <br>
Deploy OpenClaw on Alibaba Cloud ECS and integrate it with DingTalk using Alibaba Cloud Bailian for LLM responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to provision Alibaba Cloud ECS networking and compute, configure Bailian credentials, install OpenClaw, and verify a DingTalk bot integration for users to chat with the assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create billable Alibaba Cloud ECS, EIP, Bailian model, and network resources. <br>
Mitigation: Use the workflow only when those resources are intended, monitor ECS/EIP and model usage costs, and clean up resources after explicit user confirmation. <br>
Risk: The workflow handles Bailian API keys and DingTalk client credentials. <br>
Mitigation: Use dedicated least-privilege RAM users or roles, mask secrets in outputs, avoid logging full credential values, and rotate or revoke credentials when finished. <br>
Risk: The deployment downloads and runs remote NodeSource and OpenClaw installation scripts on the ECS instance. <br>
Mitigation: Review remote installation scripts before execution and keep timeout-bounded curl or wget usage in place. <br>
Risk: Broad FullAccess RAM policies are documented as a quick setup option. <br>
Mitigation: Prefer the custom least-privilege RAM policy from the bundled RAM policy guide for production deployments. <br>


## Reference(s): <br>
- [Bailian API Key Guide](references/bailian-api-key-guide.md) <br>
- [DingTalk App Setup Guide](references/dingtalk-setup-guide.md) <br>
- [RAM Policies for OpenClaw ECS DingTalk Deployment](references/ram-policies.md) <br>
- [Alibaba Cloud Deploy OpenClaw](https://help.aliyun.com/zh/simple-application-server/use-cases/quickly-deploy-and-use-openclaw) <br>
- [DingTalk Open Platform ECS Deployment](https://open.dingtalk.com/document/dingstart/deployment-alibaba-cloud-ecs-server) <br>
- [DingTalk AI Employee Setup](https://open.dingtalk.com/document/dingstart/build-dingtalk-ai-employees) <br>
- [OpenClaw Official Website](https://openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with Alibaba Cloud CLI command blocks and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes input validation, credential handling, deployment verification, cost notes, and cleanup guidance.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
