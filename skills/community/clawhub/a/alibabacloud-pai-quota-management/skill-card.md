## Description: <br>
Manages Alibaba Cloud PAI quota lifecycles with the aliyun paistudio and aiworkspace CLI, including quota CRUD, scaling, workload inspection, and workspace attachment or detachment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect, create, update, scale, delete, attach, and detach Alibaba Cloud PAI quotas while following explicit confirmation, dry-run, and permission checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact quota lifecycle operations such as create, scale, delete, attach, and detach. <br>
Mitigation: Install it only for operators authorized to manage Alibaba Cloud PAI quotas and prefer read-only or resource-scoped RAM policies unless full lifecycle changes are required. <br>
Risk: Detach and delete workflows can affect workspace access or active workloads if executed against the wrong resource. <br>
Mitigation: Verify dry-run output, active workload checks, resolved identifiers, and the exact confirmation token before each mutating operation. <br>
Risk: Using the wrong detach option can remove more than intended. <br>
Mitigation: For detach-only workflows, confirm the command uses `--option Detach` exactly before execution. <br>


## Reference(s): <br>
- [PAI Quota acceptance criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI installation guide](references/cli-installation-guide.md) <br>
- [RAM policies for PAI quota management](references/ram-policies.md) <br>
- [Related PAI quota commands](references/related-commands.md) <br>
- [PAI quota validation rules](references/validation-rules.md) <br>
- [PAI quota verification method](references/verification-method.md) <br>
- [Aliyun CLI documentation](https://help.aliyun.com/zh/cli/) <br>
- [PAI quota resource management documentation](https://help.aliyun.com/zh/pai/user-guide/ai-computing-resource-management/) <br>
- [PAI Studio OpenAPI documentation](https://next.api.aliyun.com/document/PaiStudio/2022-01-12/overview) <br>
- [AIWorkSpace OpenAPI documentation](https://next.api.aliyun.com/document/AIWorkSpace/2021-02-04/overview) <br>
- [aliyun-cli-paistudio plugin source](https://github.com/aliyun/aliyun-cli-paistudio) <br>
- [aliyun-cli-aiworkspace plugin source](https://github.com/aliyun/aliyun-cli-aiworkspace) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aliyun CLI context, region, quota or workspace identifiers, and user confirmation tokens for mutating operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
