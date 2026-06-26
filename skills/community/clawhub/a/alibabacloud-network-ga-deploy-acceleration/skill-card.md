## Description: <br>
Deploy acceleration services using Alibaba Cloud Global Accelerator (GA) for cross-border Web/API, global gaming, audio/video, and enterprise application acceleration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud network engineers use this skill to plan, configure, execute, and verify Alibaba Cloud Global Accelerator deployments for cross-region traffic acceleration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help create, update, or delete paid Alibaba Cloud GA resources. <br>
Mitigation: Review every generated Aliyun command before execution and explicitly verify account identity, resource IDs, billing mode, billing impact, and deletion impact. <br>
Risk: Cloud credentials or access keys could be mishandled during setup. <br>
Mitigation: Use a dedicated least-privilege RAM user or temporary credentials, configure secrets outside the chat, and avoid passing access keys directly in commands. <br>
Risk: Incorrect parameters can misconfigure cross-border routing, listeners, endpoint groups, or forwarding rules. <br>
Mitigation: Confirm all user-configurable parameters, validate API metadata before command generation, and wait for GA resources to become active after each creation step. <br>
Risk: Acceleration performance claims can be misleading without real measurements. <br>
Mitigation: Base performance conclusions only on actual test data from the documented online dial test, curl checks, or UDP test tool. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-network-ga-deploy-acceleration) <br>
- [GA Operational Important Notes](references/important-notes.md) <br>
- [API and CLI Command Reference](references/related-apis.md) <br>
- [RAM Permission Policies for GA Deployment](references/ram-policies.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [GA Acceleration Performance Verification Guide](references/acceleration-test-guide.md) <br>
- [Alibaba Cloud Global Accelerator Documentation](https://help.aliyun.com/zh/ga/) <br>
- [Alibaba Cloud GA API Metadata](https://api.aliyun.com/product/Ga) <br>
- [Alibaba Cloud Network Dial Test Guide](https://help.aliyun.com/zh/ga/use-cases/use-the-network-dial-test-tool-to-test-the-acceleration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes execution plans, Aliyun CLI commands, configuration summaries, status checks, and verification guidance.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
