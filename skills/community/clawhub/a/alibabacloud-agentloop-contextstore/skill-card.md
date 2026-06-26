## Description: <br>
Operate Alibaba Cloud CloudMonitor Service (CMS) AgentLoop ContextStore by using aliyun CLI with api version 2024-03-30. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud CMS AgentLoop ContextStore resources, including memory and experience stores, context records, and store API keys through the Aliyun CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through operations that create, update, or delete Alibaba Cloud CMS ContextStore resources. <br>
Mitigation: Use a least-privilege RAM identity and require explicit user confirmation before any write, API key, bulk delete, or store deletion operation. <br>
Risk: Credential exposure could occur if access keys or secret values are pasted into chat, command history, or logs. <br>
Mitigation: Do not paste access keys into the session, use external credential configuration, and verify identity state with non-secret CLI status commands. <br>
Risk: Broad CLI plugin setup and automatic plugin behavior can expand the operational surface beyond the immediate ContextStore task. <br>
Mitigation: Review and pin CLI plugins where possible, verify the CMS plugin version, and install only when Alibaba Cloud ContextStore administration is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-agentloop-contextstore) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CLI Installation Guide](artifact/references/cli-installation-guide.md) <br>
- [Context Data Operations](artifact/references/context-data-operations.md) <br>
- [Filter Syntax](artifact/references/filter-syntax.md) <br>
- [RAM Policies](artifact/references/ram-policies.md) <br>
- [Related Commands](artifact/references/related-commands.md) <br>
- [Store Management](artifact/references/store-management.md) <br>
- [Verification Method](artifact/references/verification-method.md) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/) <br>
- [Aliyun CLI repository](https://github.com/aliyun/aliyun-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation for configurable parameters and destructive operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
