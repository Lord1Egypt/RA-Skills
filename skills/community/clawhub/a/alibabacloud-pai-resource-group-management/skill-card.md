## Description: <br>
End-to-end Alibaba Cloud PAI ResourceGroup lifecycle management via `aliyun paistudio`, covering ResourceGroup list, get, create, update, delete, read-only MachineGroup inspection, and UserVpc bind/unbind workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to inspect and manage Alibaba Cloud PAI ResourceGroups, MachineGroups, and VPC bindings through the Aliyun `paistudio` CLI. It is intended for guarded cloud administration workflows that require least-privilege access and explicit confirmation before mutating resource groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through Alibaba Cloud PAI ResourceGroup create, update, and delete operations. <br>
Mitigation: Install only when this authority is intended, use least-privilege RAM policies, and keep the skill's confirmation gates for every mutating operation. <br>
Risk: Incorrect or untrusted local Aliyun CLI or paistudio plugin setup could affect cloud operation behavior. <br>
Mitigation: Verify the Aliyun CLI and paistudio plugin source and version before enabling auto-install or updating. <br>
Risk: MachineGroup release is billing-impacting and outside the skill's supported automation boundary. <br>
Mitigation: Keep MachineGroup deletion disabled in the agent workflow and direct users to the PAI Console or appropriate billing flow for release actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-pai-resource-group-management) <br>
- [Public PAI OpenAPI portal](https://next.api.aliyun.com/document/PaiStudio/2022-01-12/overview) <br>
- [PAI AI Computing Resource Management](https://help.aliyun.com/zh/pai/user-guide/ai-computing-resource-management/) <br>
- [Custom RAM Authorization Policy](https://help.aliyun.com/zh/pai/user-guide/configure-custom-ram-authorization-policy) <br>
- [PAI Console](https://pai.console.aliyun.com/) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Pre-execution Validation Rules](references/validation-rules.md) <br>
- [Confirmation Gate](references/confirmation-gate.md) <br>
- [NOT Implementable / Forbidden via this skill](references/not-implementable.md) <br>
- [Verification Method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and structured confirmation blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aliyun CLI and paistudio plugin context; mutating operations are gated by explicit user confirmation.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
