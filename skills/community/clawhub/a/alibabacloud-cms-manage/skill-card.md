## Description: <br>
Guides agents through Alibaba Cloud CloudMonitor (CMS) management with the aliyun cms2 CLI, including monitoring onboarding, metrics, APM, RUM, event, and alerting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and cloud operations teams use this skill to inspect and manage Alibaba Cloud CMS resources, configure observability onboarding, query monitoring data, and manage alerting workflows through the aliyun cms2 CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, update, delete, enable, disable, or otherwise mutate Alibaba Cloud CMS resources using configured aliyun credentials. <br>
Mitigation: Install it only for intended CMS management use, grant least-privilege RAM permissions, and require careful confirmation of every proposed write command before execution. <br>
Risk: Broad permissions such as cross-account proxy or tag mutation can expand the blast radius of an incorrect command. <br>
Mitigation: Avoid granting cross-account proxy or tag mutation unless the workflow explicitly requires it, and trim RAM policy resources and actions to the target operational scope. <br>
Risk: Important prompts and summaries may be presented in Simplified Chinese. <br>
Mitigation: Use the skill only where operators can review the Chinese-language summaries and exact commands before approving cloud-side changes. <br>


## Reference(s): <br>
- [Alibaba Cloud CLI install guide](https://help.aliyun.com/document_detail/121541.html) <br>
- [Alibaba Cloud CLI update guide](https://help.aliyun.com/zh/cli/update-cli) <br>
- [Integration module reference](references/integration.md) <br>
- [Alerting module reference](references/alerting.md) <br>
- [Application Monitoring module reference](references/apm.md) <br>
- [Real User Monitoring module reference](references/rum.md) <br>
- [RAM policy reference](references/ram-policies.md) <br>
- [Related API inventory](assets/related_apis.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [User-facing explanations are expected in Simplified Chinese while CLI commands, flags, IDs, JSON fields, and error text remain verbatim.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
