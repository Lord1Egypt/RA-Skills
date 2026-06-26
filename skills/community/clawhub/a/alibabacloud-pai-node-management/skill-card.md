## Description: <br>
Manage Alibaba Cloud PAI compute nodes by listing resource-group or quota scoped nodes, inspecting status and hardware details, and preparing safety-gated cordon, uncordon, and drain workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators and platform engineers use this skill to inspect Alibaba Cloud PAI node status and produce audited Aliyun CLI workflows for node maintenance. It is intended for controlled maintenance tasks that require scoped cloud permissions, explicit confirmation for mutating operations, and escalation for unsupported node-level actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Alibaba Cloud RAM permissions could expose more PAI resources than the operator intends. <br>
Mitigation: Use least-privilege RAM policies scoped to the specific resource groups or quotas being managed. <br>
Risk: Cordon, uncordon, and drain are real operational changes that can affect workload placement or capacity. <br>
Mitigation: Require the displayed CONFIRM-NODE-OP token and review generated operation payloads before execution. <br>
Risk: Unverified local Aliyun CLI or plugin installations could produce unexpected behavior. <br>
Mitigation: Verify Aliyun CLI and paistudio plugin provenance before using the skill in an operational environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-pai-node-management) <br>
- [PaiStudio 2022-01-12 OpenAPI](https://next.api.aliyun.com/document/PaiStudio/2022-01-12/overview) <br>
- [PAI AI Computing Resource Management](https://help.aliyun.com/zh/pai/user-guide/ai-computing-resource-management/) <br>
- [Custom RAM Authorization Policy](https://help.aliyun.com/zh/pai/user-guide/configure-custom-ram-authorization-policy) <br>
- [CLI Installation Guide](artifact/references/cli-installation-guide.md) <br>
- [RAM Policies](artifact/references/ram-policies.md) <br>
- [Confirmation Protocol](artifact/references/confirmation-protocol.md) <br>
- [Operate Node Parameters](artifact/references/operate-node-parameters.md) <br>
- [Unsupported Node Operations](artifact/references/not-implementable.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Aliyun CLI command examples and JSON operation payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit confirmation before cordon, uncordon, or drain operations; business API commands must include the prescribed user-agent string.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
