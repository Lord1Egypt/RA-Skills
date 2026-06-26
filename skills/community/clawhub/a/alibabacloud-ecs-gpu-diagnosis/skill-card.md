## Description: <br>
Diagnose Alibaba Cloud ECS GPU instances to detect GPU device status, driver issues, and hardware failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators, developers, and support engineers use this skill to validate Alibaba Cloud CLI readiness, create ECS GPU diagnostic reports, poll report status, and summarize detected GPU issues with recommended remediation steps. <br>

### Deployment Geography for Use: <br>
Alibaba Cloud ECS regions supported by the skill, including cn-hangzhou, cn-shanghai, cn-beijing, and cn-shenzhen. <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud CLI credentials to query ECS instances and create diagnostic reports. <br>
Mitigation: Use least-privilege RAM credentials with only the required ECS diagnostic and instance query permissions, and confirm the target instance and region before execution. <br>
Risk: CLI installation and update steps can modify a system-wide Alibaba Cloud CLI binary. <br>
Mitigation: Verify the CLI download source, review installation commands before running them, and prefer managed package installation where available. <br>
Risk: AI-mode changes CLI configuration for agent execution. <br>
Mitigation: Enable AI-mode only for the diagnostic workflow and disable it after success or failure as the skill instructs. <br>


## Reference(s): <br>
- [Alibaba Cloud CLI Installation Guide](references/cli-installation.md) <br>
- [RAM Permission List](references/ram-policies.md) <br>
- [Alibaba Cloud CLI official installation documentation](https://help.aliyun.com/zh/cli/install-cli) <br>
- [Alibaba Cloud GPU driver installation guide](https://help.aliyun.com/document_detail/108460.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with Alibaba Cloud CLI commands, diagnostic report details, issue summaries, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ECS instance ID, region ID, configured Alibaba Cloud CLI credentials, and RAM permissions for ECS diagnostic and instance query APIs.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
